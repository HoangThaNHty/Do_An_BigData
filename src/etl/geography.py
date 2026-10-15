"""Versioned name joins; historical district regions, never property GPS."""
import json
import re
import unicodedata
from pathlib import Path
from pyspark.sql import functions as F
from src.config.spark import ROOT

GEO_VERSION = "hcm-pre-merger-district-reference-v1"
PREFIX = r"^(?:thành phố|thị xã|thị trấn|quận|huyện|phường|xã|tp[.]?|q[.]?|h[.]?|p[.]?|x[.]?)\s+"


def key(value):
    value = re.sub(r"\s+", " ", unicodedata.normalize("NFC", value or "").lower()).strip()
    value = re.sub(PREFIX, "", value)
    return str(int(value)) if value.isdigit() else value


def ascii_name(value):
    return "".join(c for c in unicodedata.normalize("NFD", value.lower().replace("đ", "d")) if not unicodedata.combining(c))


def reference():
    raw = ROOT / "data/raw/geography"
    admin = json.loads((raw / "admin_2025_03.json").read_text(encoding="utf-8"))
    province = next(p for p in admin if p["Code"] == "79")
    districts, wards = [], []
    for district in province["District"]:
        name = key(district["FullName"])
        districts.append((name, district["Code"], district["FullName"]))
        wards.extend((district["Code"], key(w["FullName"]), w["Code"]) for w in district["Ward"])
    thu_duc = next(d for d in districts if d[0] == "thủ đức")
    districts.extend((alias, thu_duc[1], thu_duc[2]) for alias in ["2", "9"])
    assert len({d[0] for d in districts}) == len(districts)
    assert len({(w[0], w[1]) for w in wards}) == len(wards)
    return districts, wards


def attach(df, spark):
    districts, wards = reference()
    d = spark.createDataFrame(districts, "region_source_key string, district_code string, district_label string")
    w = spark.createDataFrame(wards, "district_code string, ward_reference_key string, ward_code string")
    # Spark built-ins keep the join scalable; normalizing original source fields
    # separately avoids altering frozen rule keys or original addresses.
    def expression(column):
        value = F.trim(F.regexp_replace(F.lower(F.coalesce(F.col(column), F.lit(""))), r"\s+", " "))
        value = F.regexp_replace(value, PREFIX, "")
        return F.regexp_replace(value, r"^0+([1-9][0-9]*)$", "$1")
    out = df.withColumn("region_source_key", expression("district_name")).withColumn("ward_reference_key", expression("ward_name"))
    out = out.join(F.broadcast(d), "region_source_key", "left").join(F.broadcast(w), ["district_code", "ward_reference_key"], "left")
    out = out.withColumn("geo_match_status", F.when(F.col("district_code").isNull(), "district_outside_or_unresolved")
                         .when(F.col("ward_code").isNotNull(), "district_and_ward_reference_match")
                         .when(F.col("ward_reference_key") == "", "district_match_ward_missing")
                         .otherwise("district_match_ward_other_vintage_or_unknown"))
    return out.withColumn("geo_version", F.lit(GEO_VERSION))


def export_map(output):
    from shapely import make_valid, union_all
    from shapely.geometry import shape, mapping
    districts, _ = reference()
    canonical = {code:label for _, code, label in districts}
    names = {ascii_name(key(label)):code for code,label in canonical.items()}
    names.update({"2":"769", "9":"769"})
    source = json.loads((ROOT / "data/raw/geography/districts_2020_simplified.geojson").read_text(encoding="utf-8"))
    grouped = {}
    for feature in source["features"]:
        name = ascii_name(feature["properties"]["shapeName"])
        name = re.sub(r"^quan\s+", "", name)
        if name not in names:
            continue
        geom = shape(feature["geometry"])
        # Name + spatial plausibility disambiguates homonymous districts outside HCM.
        if not (106.3 < geom.centroid.x < 107.1 and 10.1 < geom.centroid.y < 11.3):
            continue
        grouped.setdefault(names[name], []).append((make_valid(geom), feature["properties"]["shapeID"]))
    assert set(grouped) == set(canonical), (set(canonical) - set(grouped))
    assert len(grouped["769"]) == 3, "Thu Duc union must contain old districts 2, 9 and Thu Duc"
    features = []
    for code, parts in sorted(grouped.items()):
        geometry = union_all([p[0] for p in parts])
        assert geometry.is_valid and not geometry.is_empty
        features.append({"type":"Feature", "properties":{"district_code":code,"district_label":canonical[code],
                         "boundary_year":2020,"geometry_reference":"Historical simplified boundaries; Thu Duc union of 3 districts", "source_shape_ids":[p[1] for p in parts]},
                         "geometry":mapping(geometry)})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"type":"FeatureCollection", "attribution":"OCHA ROAP / Government of Viet Nam via geoBoundaries, CC BY 3.0 IGO", "features":features}, ensure_ascii=False), encoding="utf-8")
    return len(features)


if __name__ == "__main__":
    print("Map districts:", export_map(ROOT / "artifacts/geography/hcm_districts.geojson"))
