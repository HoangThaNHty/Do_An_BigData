"""Prepare a blinded random review and score only completely labelled evaluation data."""
import argparse
import csv
from datetime import datetime, timezone
import glob
import hashlib
import json
from pathlib import Path

from src.config.spark import ROOT

SOURCE_FIELDS = ["row_id", "name", "description", "property_type_name", "price_raw", "price", "area", "district_name", "ward_name", "published_at"]
LABEL_FIELDS = ["review_split", "manual_transaction", "manual_area_kind", "manual_price_valid", "manual_scope", "reviewer", "review_method", "review_notes"]


def prepare(output, size, overwrite=False, seed=20261011, quality_checks=False, evaluation_only=False, candidates_only=False):
    from pyspark.sql import functions as F
    from src.config.spark import session
    from src.etl.rules import enrich
    output.mkdir(parents=True, exist_ok=True)
    if (output / "blind_review.csv").exists() and not overwrite:
        raise FileExistsError("Review sample already exists; preserve labels or choose a new output folder.")
    spark = session("prepare-independent-review")
    try:
        files = sorted(glob.glob(str(ROOT / "data/raw/oceanng/*.parquet")))
        if not files:
            raise FileNotFoundError("Dataset not downloaded")
        raw = spark.read.parquet(*files).where((F.col("province_name") == "Hồ Chí Minh") & F.col("property_type_name").isin("Nhà", "Căn hộ chung cư"))
        # Bernoulli sample before costly text rules; uniform inclusion probability.
        # Save the selected sample: changes to partitions can change seeded sampling.
        sampled = enrich(raw.sample(False, min(1.0, size * 12 / 1122870), seed=seed))
        prior = [ROOT / "artifacts/profile/manual_review.csv"] + sorted((ROOT / "artifacts/review").glob("*/blind_review.csv"))
        ids = set()
        excluded_files = []
        for previous in prior:
            if previous.exists() and previous.resolve() != (output / "blind_review.csv").resolve():
                with previous.open(encoding="utf-8-sig") as f:
                    ids.update(r["row_id"] for r in csv.DictReader(f))
                excluded_files.append(str(previous))
        if ids:
            excluded = spark.createDataFrame([(x,) for x in sorted(ids)], ["row_id"])
            sampled = sampled.join(F.broadcast(excluded), "row_id", "left_anti")
        if quality_checks:
            from src.etl.quality import check
            sampled = check(sampled)
        if candidates_only:
            if not quality_checks:
                raise ValueError("Candidate review requires --quality-checks")
            sampled = sampled.where("protected_candidate")
        selection = sampled.dropDuplicates(["row_id"]).orderBy(F.sha2(F.concat(F.lit(f"independent-{seed}"), F.col("row_id")), 256)).limit(size)
        predictions = []
        prediction_fields = ["transaction_label", "transaction_reason", "area_kind", "area_evidence", "price_ambiguous"]
        if quality_checks:
            prediction_fields += ["price_check", "area_check", "scope_check", "candidate_eligible", "protected_candidate", "quality_reasons", "validation_status"]
        selected = selection.select(*SOURCE_FIELDS, *prediction_fields).collect()
        if len(selected) < size:
            raise ValueError(f"Only {len(selected)} rows selected; requested {size}")
        with (output / "blind_review.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=SOURCE_FIELDS + LABEL_FIELDS)
            writer.writeheader()
            for i,r in enumerate(selected):
                row = r.asDict()
                predictions.append({k: row[k] for k in ["row_id"] + prediction_fields})
                writer.writerow({**{k: row[k] for k in SOURCE_FIELDS}, "review_split": "evaluation" if evaluation_only or i % 2 else "calibration"})
        (output / "predictions.json").write_text(json.dumps(predictions, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest = {"created_at_utc":datetime.now(timezone.utc).isoformat(), "size":size, "seed":seed,
                    "excluded_review_files":excluded_files, "excluded_row_ids":len(ids), "evaluation_only":evaluation_only,
                    "population":"Protected HCM candidates excluding prior review row IDs" if candidates_only else "HCM house/apartment listings excluding prior review row IDs; unique row IDs",
                    "candidates_only":candidates_only,
                    "method":"Bernoulli subsample then stable hash selection; frozen sample, not a benchmark of assets",
                    "rules_sha256":hashlib.sha256((ROOT / "src/etl/rules.py").read_bytes()).hexdigest(),
                    "dataset_revision":json.loads((ROOT / "data/raw/oceanng/manifest.json").read_text())["revision"]}
        if quality_checks:
            manifest["quality_sha256"] = hashlib.sha256((ROOT / "src/etl/quality.py").read_bytes()).hexdigest()
        manifest["predictions_sha256"] = hashlib.sha256((output / "predictions.json").read_bytes()).hexdigest()
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Prepared {len(selected)} blinded rows; no manual labels assigned.")
    finally:
        spark.stop()


def replay_review(output, split="calibration"):
    """Preserve initial predictions and run a versioned review split."""
    from pyspark.sql import functions as F, types as T
    from src.config.spark import session
    from src.etl.rules import enrich, RULES_VERSION
    rule_hash = hashlib.sha256((ROOT / "src/etl/rules.py").read_bytes()).hexdigest()
    if split == "evaluation":
        frozen = json.loads((output / "freeze.json").read_text(encoding="utf-8"))
        if frozen["rules_sha256"] != rule_hash:
            raise ValueError("Rules differ from the frozen evaluation version")
    with (output / "blind_review.csv").open(encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f) if r["review_split"] == split]
    columns = SOURCE_FIELDS + ["province_name"]
    schema = T.StructType([T.StructField(k, T.DoubleType() if k == "area" else T.StringType(), True) for k in columns])
    records = [{**{k:r[k] or None for k in SOURCE_FIELDS}, "area":float(r["area"]) if r["area"] else None,
                "price":r["price_raw"] or None, "province_name":"Hồ Chí Minh"} for r in rows]
    # row_id is regenerated using the exact source fields; detect any drift.
    spark = session("replay-" + split)
    try:
        df = spark.createDataFrame(records, schema).withColumnRenamed("row_id", "expected_row_id")
        selected = enrich(df).select("expected_row_id", "row_id", "transaction_label", "transaction_reason",
                                    "area_kind", "area_evidence", "area_measure", "price_ambiguous",
                                    "residential_scope_reason", "candidate_eligible").collect()
        if any(r.expected_row_id != r.row_id for r in selected):
            raise ValueError("Replayed source row IDs drifted; do not align by position")
        predictions = [r.asDict() for r in selected]
    finally:
        spark.stop()
    run = output / (split + "_runs") / rule_hash[:16]
    run.mkdir(parents=True, exist_ok=True)
    (run / "predictions.json").write_text(json.dumps(predictions, ensure_ascii=False, indent=2), encoding="utf-8")
    if split == "evaluation":
        manifest = {"split":split, "rows":len(rows), "rules_version":RULES_VERSION, "rules_sha256":rule_hash,
                    "predictions_sha256":hashlib.sha256((run / "predictions.json").read_bytes()).hexdigest(),
                    "created_at_utc":datetime.now(timezone.utc).isoformat(), "status":"predictions_only_not_accuracy"}
        (run / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps(manifest, indent=2))
        return
    original = {r["row_id"]:r for r in json.loads((output / "predictions.json").read_text(encoding="utf-8"))}
    labelled = [r for r in rows if all(r[k].strip() for k in ["manual_transaction", "manual_area_kind", "manual_price_valid", "reviewer", "review_method"])]
    current = {r["row_id"]:r for r in predictions}
    def diagnostic(preds):
        return {"transaction_disagreements":sum(r["manual_transaction"] != preds[r["row_id"]]["transaction_label"] for r in labelled),
                "area_disagreements":sum(r["manual_area_kind"] != preds[r["row_id"]]["area_kind"] for r in labelled)}
    errors = [{"row_id":r["row_id"], "reference_transaction":r["manual_transaction"], "reference_area":r["manual_area_kind"],
               "prediction":current[r["row_id"]], "notes":r["review_notes"]} for r in labelled
              if r["manual_transaction"] != current[r["row_id"]]["transaction_label"] or r["manual_area_kind"] != current[r["row_id"]]["area_kind"]]
    report = {"status":"calibration_only", "rows":len(rows), "labelled":len(labelled), "rules_version":RULES_VERSION,
              "rules_sha256":rule_hash, "review_sha256":hashlib.sha256((output / "blind_review.csv").read_bytes()).hexdigest(),
              "created_at_utc":datetime.now(timezone.utc).isoformat(), "review_methods":sorted({r["review_method"] for r in labelled}),
              "initial":diagnostic(original), "current":diagnostic(current), "remaining_disagreements":errors,
              "limitations":["Calibration labels were used for rule changes; this is not independent accuracy.",
                              "AI source-text labels are not human ground truth.",
                              "Area reference may infer land from dimensions; automatic rules retain stricter explicit legal/land evidence.",
                              "Price validation is source-text corroboration, not valuation or fraud verification."]}
    (run / "diagnostic.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "remaining_disagreements"}, ensure_ascii=False, indent=2))


def score(output, predictions_path=None):
    with (output / "blind_review.csv").open(encoding="utf-8-sig") as f:
        all_rows = list(csv.DictReader(f))
    rows = [r for r in all_rows if r["review_split"] == "evaluation"]
    # Labels may change; frozen source fields and split membership may not.
    original_path = output / "blind_review.unlabelled.csv"
    if original_path.exists():
        with original_path.open(encoding="utf-8-sig", newline="") as f:
            original_rows = list(csv.DictReader(f))
        original = {r['row_id']:r for r in original_rows}
        if len(original) != len(all_rows) or {r['row_id'] for r in all_rows} != set(original):
            raise ValueError("Review source row IDs changed")
        for r in all_rows:
            if any(r[k] != original[r['row_id']][k] for k in SOURCE_FIELDS + ['review_split']):
                raise ValueError("Review source fields or split changed after preparation")
    if not rows or any(r["review_split"] not in {"evaluation", "calibration"} for r in all_rows):
        raise ValueError("Review must contain evaluation rows and valid splits")
    predictions_path = predictions_path or output / "predictions.json"
    predictions_list = json.loads(predictions_path.read_text(encoding="utf-8"))
    predictions = {r["row_id"]:r for r in predictions_list}
    if len(predictions) != len(predictions_list):
        raise ValueError("Duplicate prediction row IDs")
    provenance = {"path":str(predictions_path), "sha256":hashlib.sha256(predictions_path.read_bytes()).hexdigest()}
    prediction_manifest_path = predictions_path.parent / "manifest.json"
    is_initial = predictions_path.resolve() == (output / "predictions.json").resolve()
    if is_initial and prediction_manifest_path.exists():
        initial_manifest = json.loads(prediction_manifest_path.read_text(encoding="utf-8"))
        if "predictions_sha256" in initial_manifest and initial_manifest["predictions_sha256"] != provenance["sha256"]:
            raise ValueError("Prepared review prediction fingerprint mismatch")
        provenance["rules_sha256"] = initial_manifest.get("rules_sha256")
        if "quality_sha256" in initial_manifest:
            provenance["quality_sha256"] = initial_manifest["quality_sha256"]
    if not is_initial:
        prediction_manifest = json.loads(prediction_manifest_path.read_text(encoding="utf-8"))
        frozen = json.loads((output / "freeze.json").read_text(encoding="utf-8"))
        if (prediction_manifest["split"] != "evaluation" or prediction_manifest["rules_sha256"] != frozen["rules_sha256"]
                or prediction_manifest["predictions_sha256"] != provenance["sha256"]):
            raise ValueError("Evaluation prediction provenance does not match frozen rules")
        provenance["rules_sha256"] = prediction_manifest["rules_sha256"]
    if len({r['row_id'] for r in all_rows}) != len(all_rows):
        raise ValueError("Duplicate review row IDs")
    if any(r["row_id"] not in predictions for r in rows):
        raise ValueError("Review row missing prediction")
    required = ["manual_transaction", "manual_area_kind", "manual_price_valid", "reviewer", "review_method"]
    has_scope = "manual_scope" in rows[0]
    if has_scope:
        required.append("manual_scope")
    missing = [r["row_id"] for r in rows if any(not r[k].strip() for k in required)]
    report = {"evaluation_rows":len(rows), "fully_labelled_rows":len(rows)-len(missing),
              "status":"needs_labels" if missing else "ready", "metrics":None, "prediction_provenance":provenance,
              "review_sha256":hashlib.sha256((output / "blind_review.csv").read_bytes()).hexdigest(),
              "limitations":["Reference labels require source-text reading; record human or AI method honestly.",
                             "Results apply to this review sample, not automatically to all market listings."]}
    if not missing and rows:
        allowed = {"manual_transaction":{"sale","rent","uncertain"}, "manual_area_kind":{"apartment","land","floor","unknown"},
                   "manual_price_valid":{"yes","no","uncertain"}, "review_method":{"human","ai_assisted","ai"}}
        if has_scope:
            allowed["manual_scope"] = {"residential", "outside", "uncertain"}
        for r in rows:
            for k,values in allowed.items():
                if r[k] not in values:
                    raise ValueError(f"Invalid {k}: {r[k]}")
        confusion = {a:{b:0 for b in ["sale","rent","uncertain"]} for a in ["sale","rent","uncertain"]}
        predicted_sales = 0
        sale_correct = 0
        area_correct = 0
        for r in rows:
            pred = predictions[r["row_id"]]
            confusion[r["manual_transaction"]][pred["transaction_label"]] += 1
            if pred["transaction_label"] == "sale":
                predicted_sales += 1
                sale_correct += r["manual_transaction"] == "sale"
            area_correct += r["manual_area_kind"] == pred["area_kind"]
        report["metrics"] = {"confusion_actual_then_predicted":confusion, "predicted_sale_count":predicted_sales,
                            "sale_precision":sale_correct/predicted_sales if predicted_sales else None,
                            "area_kind_agreement":area_correct/len(rows)}
        if predictions_list and "protected_candidate" in predictions_list[0]:
            kept = [r for r in rows if predictions[r["row_id"]]["protected_candidate"]]
            def supported(r):
                expected_area = "land" if r["property_type_name"] == "Nhà" else "apartment"
                return (r["manual_transaction"] == "sale" and r["manual_price_valid"] == "yes"
                        and r["manual_area_kind"] == expected_area)
            count = sum(supported(r) for r in kept)
            report["metrics"]["quality_candidates"] = {
                "count": len(kept), "source_text_supported_count": count,
                "source_text_support_rate": count / len(kept) if kept else None,
                "unsupported_row_ids": [r["row_id"] for r in kept if not supported(r)]}
            if has_scope:
                scope_supported = sum(supported(r) and r["manual_scope"] == "residential" for r in kept)
                report["metrics"]["quality_candidates"].update(
                    scope_supported_count=scope_supported,
                    scope_support_rate=scope_supported / len(kept) if kept else None,
                    scope_unsupported_row_ids=[r["row_id"] for r in kept if not (supported(r) and r["manual_scope"] == "residential")])
                if kept:
                    n, p, z = len(kept), scope_supported / len(kept), 1.959963984540054
                    center = (p + z*z/(2*n))/(1 + z*z/n)
                    radius = z*((p*(1-p)/n + z*z/(4*n*n))**0.5)/(1 + z*z/n)
                    report['metrics']['quality_candidates']['scope_support_wilson95'] = [center-radius, center+radius]
            report["limitations"].append("Candidate support checks sale, price and area reference labels only; scope, identity and fraud remain unverified.")
        report["review_methods"] = sorted({r["review_method"] for r in rows})
    (output / "evaluation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["prepare", "score", "replay-calibration", "replay-evaluation"])
    p.add_argument("--output", type=Path, default=ROOT / "artifacts/review/v1")
    p.add_argument("--size", type=int, default=300)
    p.add_argument("--seed", type=int, default=20261011)
    p.add_argument("--quality-checks", action="store_true")
    p.add_argument("--evaluation-only", action="store_true")
    p.add_argument("--candidates-only", action="store_true")
    p.add_argument("--predictions", type=Path, help="Versioned evaluation predictions for scoring")
    args = p.parse_args()
    if args.action == "prepare":
        if args.size < 2:
            p.error("size must be at least 2")
        prepare(args.output,args.size,seed=args.seed,quality_checks=args.quality_checks,evaluation_only=args.evaluation_only,candidates_only=args.candidates_only)
    elif args.action == "replay-calibration":
        replay_review(args.output)
    elif args.action == "replay-evaluation":
        replay_review(args.output, "evaluation")
    else:
        score(args.output, args.predictions)
