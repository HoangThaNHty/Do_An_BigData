"""Versioned ETL preserving quarantined rows and explicit provisional status."""
import argparse
import glob
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from pyspark import StorageLevel
from pyspark.sql import functions as F
from src.config.spark import ROOT, session
from src.etl.rules import enrich, RULES_VERSION
from src.etl.quality import check, QUALITY_VERSION


def records(df):
    return [r.asDict(recursive=True) for r in df.collect()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/etl_v1")
    args = parser.parse_args()
    output = args.output.resolve()
    output.relative_to((ROOT / "data/processed").resolve())
    if output.exists():
        raise FileExistsError("Preserve prior ETL runs; use a new --output directory")
    spark = session("HCM-versioned-ETL")
    started = time.perf_counter()
    try:
        files = sorted(glob.glob(str(ROOT / "data/raw/oceanng/*.parquet")))
        if not files:
            raise FileNotFoundError("No source Parquet files")
        raw = spark.read.parquet(*files).where((F.col("province_name") == "Hồ Chí Minh") & F.col("property_type_name").isin("Nhà", "Căn hộ chung cư"))
        raw_count = raw.count()
        original_fields = raw.columns
        source = raw.withColumn("source_record_id", F.sha2(F.to_json(F.struct(*original_fields), options={"ignoreNullFields":"false"}), 256)).dropDuplicates(["source_record_id"])
        data = check(enrich(source)).persist(StorageLevel.DISK_ONLY)
        unique_count = data.count()
        print(f"Source {raw_count}; exact unique source records {unique_count}", flush=True)
        conflicts = data.groupBy("row_id").count().withColumnRenamed("count", "row_id_record_count")
        routed = data.join(conflicts, "row_id", "left")
        routed = routed.withColumn("quality_reasons", F.when(F.col("row_id_record_count") > 1,
                         F.concat("quality_reasons", F.array(F.lit("identity_attribute_conflict")))).otherwise(F.col("quality_reasons")))
        routed = routed.withColumn("protected_candidate", F.col("protected_candidate") & (F.col("row_id_record_count") == 1))
        routed = routed.withColumn("disposition", F.when(F.col("protected_candidate"), "provisional_training")
                                  .when(F.col("transaction_label") == "rent", "excluded_rent")
                                  .otherwise("quarantine"))
        # Materialize once; later aggregations read the actual written artifact.
        print("Writing audited Parquet with provisional/quarantine dispositions...", flush=True)
        routed.write.mode("errorifexists").partitionBy("disposition", "property_type_name", "published_month").parquet(str(output / "listings"))
        data.unpersist()
        written = spark.read.parquet(str(output / "listings"))
        written_count = written.count()
        if written_count != unique_count:
            raise AssertionError("ETL routing lost or duplicated records")
        summary = {"generated_at_utc":datetime.now(timezone.utc).isoformat(), "source_rows":raw_count,
                   "unique_source_records":unique_count, "exact_duplicates_removed":raw_count-unique_count,
                   "written_rows":written_count, "rules_version":RULES_VERSION, "quality_version":QUALITY_VERSION,
                   "rules_sha256":hashlib.sha256((ROOT / "src/etl/rules.py").read_bytes()).hexdigest(),
                   "quality_sha256":hashlib.sha256((ROOT / "src/etl/quality.py").read_bytes()).hexdigest(),
                   "dataset_revision":json.loads((ROOT / "data/raw/oceanng/manifest.json").read_text())["revision"],
                   "dispositions":records(written.groupBy("disposition", "property_type_name").count().orderBy("disposition", "property_type_name")),
                   "reason_counts":records(written.select(F.explode("quality_reasons").alias("reason")).groupBy("reason").count().orderBy(F.desc("count"))),
                   "price_checks":records(written.groupBy("price_check").count().orderBy(F.desc("count"))),
                   "protected_months":records(written.where("protected_candidate").groupBy("property_type_name", "published_month").count().orderBy("property_type_name", "published_month")),
                   "identity_conflict_records":written.where("row_id_record_count > 1").count(),
                   "validation_status":"provisional_requires_new_review",
                   "limitations":["Cross-field checks were designed after v1 evaluation; require a new independent sample.",
                                  "Numeric text matching does not prove a unique asset, genuine listing, or residential scope.",
                                  "No administrative boundary match, train/test split, imputation or model fitting performed.",
                                  "Same-asset reposts remain for subsequent leakage analysis; only identical source records deduplicated."]}
        summary["elapsed_seconds"] = round(time.perf_counter()-started, 2)
        (output / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        artifact = ROOT / "artifacts/etl" / output.name
        artifact.mkdir(parents=True, exist_ok=True)
        (artifact / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k:summary[k] for k in ["source_rows", "unique_source_records", "written_rows", "dispositions", "elapsed_seconds", "validation_status"]}, ensure_ascii=False, indent=2))
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
