"""Research cohort, name joins, repost groups, temporal split and aggregates."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from pyspark.sql import functions as F, Window
from src.config.spark import ROOT, session
from src.etl.geography import attach, export_map, GEO_VERSION


def reposts(df):
    # Exact normalized whole-text matches are a conservative repost proxy.
    # Removing currency values allows price revisions; dates/target never enter
    # model features. This cannot detect every same-asset ad by another broker.
    from src.etl.quality import AMOUNT
    def normalized(column):
        text = F.lower(F.coalesce(F.col(column), F.lit("")))
        text = F.regexp_replace(text, AMOUNT, " <amount> ")
        text = F.regexp_replace(text, r"\[phone_number\]|(?:\+?84|0)[0-9 .-]{8,15}", " <contact> ")
        return F.trim(F.regexp_replace(text, r"\s+", " "))
    out = df.withColumn("repost_group", F.sha2(F.to_json(F.struct(normalized("name").alias("title"), normalized("description").alias("body"),
                              "property_type_name", "district_code", "ward_reference_key", "area"), options={"ignoreNullFields":"false"}), 256))
    ordering = Window.partitionBy("repost_group").orderBy("published_ts", "source_record_id")
    return out.withColumn("repost_rank", F.row_number().over(ordering))


def temporal(df):
    return df.withColumn("split", F.when(F.col("published_month").between("2025-06", "2025-11"), "train")
                         .when(F.col("published_month") == "2025-12", "validation")
                         .when(F.col("published_month").between("2026-01", "2026-03"), "test").otherwise("outside_period"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--etl", type=Path, default=ROOT / "data/processed/etl_v4")
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/core_v1")
    parser.add_argument("--review", type=Path, default=ROOT / "artifacts/review/v5")
    args = parser.parse_args()
    output = args.output.resolve()
    output.relative_to((ROOT / "data/processed").resolve())
    if output.exists():
        raise FileExistsError("Use a new cohort version, do not overwrite")
    etl_manifest = json.loads((args.etl / "manifest.json").read_text(encoding="utf-8"))
    review = json.loads((args.review / "evaluation.json").read_text(encoding="utf-8"))
    if review["status"] != "ready" or review["fully_labelled_rows"] < 80:
        raise ValueError("At least 80 completed fresh candidate reviews required")
    if review["prediction_provenance"].get("quality_sha256") != etl_manifest["quality_sha256"]:
        raise ValueError("Candidate review and ETL use different quality code")
    quality = review["metrics"]["quality_candidates"]
    if hashlib.sha256((args.review/'blind_review.csv').read_bytes()).hexdigest() != review['review_sha256']:
        raise ValueError('Review labels changed after scoring')
    if quality.get("scope_support_rate", 0) < 0.95:
        raise ValueError("Fresh scope-inclusive candidate support below research acceptance threshold 95%; review scope first")
    spark = session("HCM-research-cohort-and-aggregates")
    try:
        all_rows = attach(spark.read.parquet(str(args.etl / "listings")).where("disposition = 'provisional_training'"), spark)
        raw_candidates = all_rows.where("protected_candidate")
        counts = {"protected_before_geo":raw_candidates.count(),
                  "candidate_geo_status":[r.asDict() for r in raw_candidates.groupBy("geo_match_status").count().collect()]}
        # Keep all previously inspected review rows outside price experiments;
        # this also removes known review errors without selective row repair.
        inspected=set()
        inspected_sources=[]
        for file in [ROOT/'artifacts/profile/manual_review.csv']+sorted((ROOT/'artifacts/review').glob('*/blind_review.csv')):
            if file.exists():
                inspected_sources.append({'path':str(file.resolve()),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
                with file.open(encoding='utf-8-sig',newline='') as handle:
                    inspected.update(row['row_id'] for row in csv.DictReader(handle))
        if inspected:
            excluded=spark.createDataFrame([(row,) for row in sorted(inspected)],['row_id'])
            raw_candidates=raw_candidates.join(F.broadcast(excluded),'row_id','left_anti')
        counts['inspected_review_ids_excluded']=len(inspected)
        counts['protected_after_review_exclusion']=raw_candidates.count()
        # District membership is required. Missing/new-vintage wards remain as
        # original names, with explicit status; no fabricated crosswalk.
        matched = raw_candidates.where("district_code IS NOT NULL")
        counts["district_matched_candidates"] = matched.count()
        grouped = temporal(reposts(matched))
        conflicts = grouped.groupBy("repost_group").agg(F.countDistinct("split").alias("split_count"), F.count("*").alias("rows"))
        counts["cross_period_repost_groups"] = conflicts.where("split_count > 1").count()
        cohort = grouped.where("repost_rank = 1 AND split != 'outside_period'")
        print("Writing geographically matched cohort with earliest record per normalized text group", flush=True)
        cohort.write.mode("errorifexists").partitionBy("split", "property_type_name").parquet(str(output / "listings"))
        (output/'excluded_review_ids.json').write_text(json.dumps(sorted(inspected)),encoding='utf-8')
        saved = spark.read.parquet(str(output / "listings"))
        counts["cohort_rows"] = saved.count()
        counts["removed_reposts_or_outside_period"] = counts["district_matched_candidates"] - counts["cohort_rows"]
        counts["split_counts"] = [r.asDict() for r in saved.groupBy("split", "property_type_name").count().orderBy("split", "property_type_name").collect()]
        assert saved.groupBy("repost_group").agg(F.countDistinct("split").alias("n")).where("n > 1").count() == 0
        artifact = ROOT / "artifacts/market"
        artifact.mkdir(parents=True, exist_ok=True)
        # Aggregates use the reviewed cohort; describe selection bias in the UI.
        median = lambda column: F.percentile_approx(column, 0.5, 10000)
        groups = {"by_district":["district_code","district_label","property_type_name"],
                  "by_month":["published_month","property_type_name"],
                  "district_month":["district_code","district_label","published_month","property_type_name"]}
        for name, columns in groups.items():
            result = saved.groupBy(*columns).agg(F.count("*").alias("count"), median("price").alias("median_price_vnd"),
                         median("area").alias("median_area_m2"), median("unit_price_vnd").alias("median_unit_price_vnd"))
            (artifact / (name + ".json")).write_text(json.dumps([r.asDict() for r in result.orderBy(*columns).collect()], ensure_ascii=False, indent=2), encoding="utf-8")
        export_map(ROOT / "artifacts/geography/hcm_districts.geojson")
        manifest = {**counts,"source_etl":str(args.etl.resolve()), "etl_quality_sha256":etl_manifest["quality_sha256"],
                    "review_sha256":review["review_sha256"], "review_method":review.get("review_methods"), "review_support":quality,
                    "inspected_review_sources":inspected_sources,
                    "geo_version":GEO_VERSION,"core_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "status":"research_cohort_ai_reference_not_human_verified", "limitations":[
                        "AI source-text references and sample support do not certify all records.",
                        "Scope limited to pre-merger HCM district regions; names matched, property addresses unverified.",
                        "Only normalized complete-text repost proxy deduplicated; other same-asset ads may cross splits.",
                        "Earliest retained group record; later repeated records excluded, changing temporal population.",
                        "Market aggregates describe this selected source cohort, not all transactions or total market."]}
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(counts, ensure_ascii=False, indent=2))
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
