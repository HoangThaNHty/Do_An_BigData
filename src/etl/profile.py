"""Full-data Spark profiling and an unlabelled manual-review sample."""
import argparse
import csv
import glob
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from pyspark.sql import functions as F
from pyspark import StorageLevel
from src.config.spark import ROOT, session
from src.etl.rules import enrich


def rows(df):
    return [r.asDict(recursive=True) for r in df.collect()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(ROOT / "data/raw/oceanng/*.parquet"))
    p.add_argument("--output", default=str(ROOT / "artifacts/profile"))
    p.add_argument("--sample-per-group", type=int, default=30)
    args = p.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    spark = session("HCM-real-estate-profile")
    started = time.perf_counter()
    try:
        files = sorted(glob.glob(args.input))
        if not files:
            raise FileNotFoundError(f"No Parquet input files: {args.input}")
        raw = spark.read.parquet(*files)
        hcm = raw.where(F.col("province_name") == "Hồ Chí Minh")
        nulls = hcm.agg(F.count("*").alias("rows"), *[
            F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in raw.columns
        ]).first().asDict()
        numeric = hcm.withColumn("price", F.col("price").cast("double"))
        stats = numeric.agg(*[expr for c in ["price", "area", "bedroom_count", "bathroom_count", "floor_count", "road_width"]
                          for expr in [F.min(c).alias(c + "_min"), F.max(c).alias(c + "_max")]]).first().asDict()
        data = enrich(hcm).persist(StorageLevel.DISK_ONLY)
        print("Profiling candidate rules over full HCM data...", flush=True)
        summary = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "input": args.input, "scope": "exact province_name Hồ Chí Minh; no historical boundary match yet",
            "schema": raw.schema.jsonValue(), "total_rows": raw.count(), "hcm_rows": nulls.pop("rows"),
            "null_counts_hcm": nulls, "numeric_extremes_hcm": stats,
            "province_counts": rows(raw.groupBy("province_name").count().orderBy(F.desc("count"))),
            "property_counts_hcm": rows(data.groupBy("property_type_name").count().orderBy(F.desc("count"))),
            "month_counts_hcm": rows(data.groupBy("published_month").count().orderBy("published_month")),
            "transaction_counts": rows(data.groupBy("transaction_label", "transaction_reason").count().orderBy(F.desc("count"))),
            "area_counts": rows(data.groupBy("property_type_name", "area_kind", "area_evidence").count().orderBy(F.desc("count"))),
            "candidate_counts": rows(data.groupBy("property_type_name", "candidate_eligible").count().orderBy(F.desc("count"))),
            "district_counts": rows(data.groupBy("district_name").count().orderBy(F.desc("count"))),
            "limitations": ["Rule labels are unvalidated candidates, not ground truth.",
                             "Apartment area semantics and house area extraction require review.",
                             "No administrative boundary mapping has been verified.",
                             "Null counts do not include empty strings or NaN; inspect separately before ETL."]
        }
        # Stable hash ordering: review sample is reproducible; group quotas are not population weights.
        from pyspark.sql.window import Window
        fields = ["row_id", "name", "description", "property_type_name", "price", "area", "district_name", "ward_name", "published_at",
                  "transaction_label", "transaction_reason", "price_ambiguous", "area_kind", "area_evidence", "candidate_eligible"]
        unique = data.dropDuplicates(["row_id"])
        window = Window.partitionBy("transaction_reason", "property_type_name", "area_evidence").orderBy(F.sha2(F.concat(F.lit("review-v1"), F.col("row_id")), 256))
        sample = unique.withColumn("review_rank", F.row_number().over(window)).where(F.col("review_rank") <= args.sample_per_group)
        with (output / "manual_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields + ["review_split", "manual_transaction", "manual_area_kind", "manual_price_valid", "review_notes"])
            writer.writeheader()
            for r in sample.select(*fields, "review_rank").toLocalIterator():
                record = r.asDict()
                rank = record.pop("review_rank")
                record["review_split"] = "evaluation" if rank % 3 == 0 else "calibration"
                writer.writerow(record)
        summary["elapsed_seconds"] = round(time.perf_counter() - started, 2)
        (output / "profile.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        data.unpersist()
        print(json.dumps({k: summary[k] for k in ["total_rows", "hcm_rows", "property_counts_hcm", "candidate_counts", "elapsed_seconds"]}, ensure_ascii=False, indent=2))
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
