"""Apply explicit source-read annotations; never infer labels from predictions."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def apply(review_dir, annotations_path, split):
    path = review_dir / "blind_review.csv"
    original = path.read_bytes()
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    selected = [r for r in rows if r["review_split"] == split]
    annotations = json.loads(annotations_path.read_text(encoding="utf-8"))
    if "manual_scope" in fields and any("scope" not in a for a in annotations):
        raise ValueError("This review requires explicit source-read scope annotations")
    seen = set()
    allowed = [{"sale", "rent", "uncertain"}, {"apartment", "land", "floor", "unknown"}, {"yes", "no", "uncertain"}]
    for a in annotations:
        index = a["index"]
        if not isinstance(index, int) or index < 0 or index >= len(selected) or index in seen:
            raise ValueError(f"Invalid/duplicate split index: {index}")
        seen.add(index)
        row = selected[index]
        if row["reviewer"].strip():
            raise ValueError(f"Already reviewed: {index}; do not overwrite annotations")
        for value, values in zip([a["transaction"], a["area_kind"], a["price_valid"]], allowed):
            if value not in values:
                raise ValueError(f"Invalid label: {value}")
        if not a["notes"].strip():
            raise ValueError("Evidence notes required")
        row.update(manual_transaction=a["transaction"], manual_area_kind=a["area_kind"],
                   manual_price_valid=a["price_valid"], reviewer="Codex-source-text-review",
                   review_method="ai", review_notes=a["notes"])
        if "manual_scope" in fields:
            if a["scope"] not in {"residential", "outside", "uncertain"}:
                raise ValueError("Invalid scope reference label")
            row["manual_scope"] = a["scope"]
    backup = review_dir / "blind_review.unlabelled.csv"
    if not backup.exists():
        backup.write_bytes(original)
    temporary = path.with_suffix(".csv.part")
    with temporary.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)
    print(json.dumps({"split": split, "applied": len(annotations), "annotations_sha256": hashlib.sha256(annotations_path.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("annotations", type=Path)
    p.add_argument("--review-dir", type=Path, default=Path("artifacts/review/v1"))
    p.add_argument("--split", choices=["calibration", "evaluation"], default="calibration")
    args = p.parse_args()
    apply(args.review_dir, args.annotations, args.split)
