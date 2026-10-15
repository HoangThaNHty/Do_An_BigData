"""Conservative, auditable candidate rules. Labels require manual validation."""
from pyspark.sql import functions as F

RULES_VERSION = "candidate-v2-frozen-for-evaluation"
SALE = r"(?:^|\s)(?:cần bán|chính chủ bán|bán gấp|bán nhanh|bán|chuyển nhượng)\s+(?:(?:lại|gấp|nhanh)\s+)?(?:nhà|căn|chung cư|biệt thự|đất|shophouse|lô|tòa nhà|toà nhà|ch\b|cc\b|penthouse|penhouse|góc\b|giá\b)"
RENT = r"(?:cho thuê|cần cho thuê|giá thuê)"
RENT_CONTEXT = r"(?:đang|hiện|sẵn|tiện|thích hợp|phù hợp|vừa ở vừa|đầu tư|có thể|khả năng|sẵn dòng tiền)\s+(?:để\s+)?(?:(?:kinh doanh|cho gia đình)\s+(?:(?:hoặc|hay|và)\s+)?)?cho thuê|cho thuê\s+dòng tiền|(?:nhận|nhận kí gửi|nhận ký gửi)\s+cho thuê|cho chuyển sang cho thuê"
DUAL = r"(?:bán\s*(?:hoặc|hay|/)\s*(?:cho\s*)?thuê|(?:cho\s*)?thuê\s*(?:hoặc|hay|/)\s*bán)"
PARTIAL = r"(?:trả trước|thanh toán trước|chỉ cần\s*(?:trả|đóng)|giá\s*(?:thuê|cọc))"
UNIT_PRICE = r"(?:triệu|tr|tỷ)\s*(?:đồng\s*)?[/]\s*(?:m2|m²|mét)"


def enrich(df):
    # Actual Parquet stores price as string, despite the dataset card's float64.
    # Cast explicitly: Spark comparison with integer literal 0 can otherwise
    # coerce a string price to int32 and turn billion-VND values into NULL.
    df = df.withColumn("price_raw", F.col("price")).withColumn("price", F.col("price").cast("double"))
    title = F.lower(F.coalesce(F.col("name"), F.lit("")))
    body = F.lower(F.coalesce(F.col("description"), F.lit("")))
    text = F.concat_ws(" ", title, body)
    title_intent = F.regexp_replace(title, r"(?:không|chưa)\s+bán|buôn bán|kinh doanh mua bán", " ")
    sale_title = (title_intent.rlike(SALE)
                  | title_intent.rlike(r"(?:^|\s)(?:bán|giá bán|hạ giá bán lỗ)(?:\s|[-:])")
                  | title_intent.rlike(r"(?:nhà|căn hộ)(?:\s+riêng)?\s+bán\b"))
    rent_title = F.regexp_replace(title, RENT_CONTEXT, " ").rlike(RENT)
    sale_body = (body.rlike(SALE) | body.rlike(r"(?:^|\s)giá bán\s*[:=]?")
                 | body.rlike(r"(?:nhà|căn hộ)\s+(?:còn\s+)?bán\b"))
    rent_body = F.regexp_replace(body, RENT_CONTEXT, " ").rlike(RENT)
    dual = text.rlike(DUAL)
    price_ambiguous = text.rlike(PARTIAL) | text.rlike(UNIT_PRICE)
    reason = (F.when(dual, "dual_transaction")
              .when(sale_title & rent_title & body.rlike(r"(?:đang\s+cho thuê|hợp\s+(?:đồng\s+)?cho thuê|dòng tiền)"), "sale_title")
              .when(sale_title & rent_title, "mixed_title")
              .when(rent_title, "rental_title")
              .when(sale_title, "sale_title")
              .when(sale_body & ~rent_body, "sale_body_only")
              .when(rent_body & ~sale_body, "rental_body_only")
              .otherwise("insufficient_evidence"))
    out = df.withColumn("transaction_reason", reason)
    out = out.withColumn("transaction_label",
                         F.when(F.col("transaction_reason").isin("sale_title", "sale_body_only"), "sale")
                         .when(F.col("transaction_reason").isin("rental_title", "rental_body_only"), "rent")
                         .otherwise("uncertain"))
    out = out.withColumn("price_ambiguous", price_ambiguous)
    out = out.withColumn("rules_version", F.lit(RULES_VERSION))
    # Do not reject a sale merely because its description gives rental income.
    # price_ambiguous is a separate, conservative training eligibility flag.
    apartment = F.col("property_type_name") == "Căn hộ chung cư"
    house = F.col("property_type_name") == "Nhà"
    # Source type can disagree with the actual listing. Explicit contradictory
    # titles are quarantined; do not call this a fully validated scope classifier.
    scope_reason = (F.when(title.rlike(r"\b(?:officetel|office tel)\b"), "officetel_requires_review")
                    .when(house & title.rlike(r"\bbiệt thự\b"), "villa_outside_primary_scope")
                    .when(house & title.rlike(r"\b(?:tòa nhà|toà nhà)\b"), "building_requires_review")
                    .when(house & title.rlike(r"(?:khách sạn|\bchdv\b|căn hộ dịch vụ)"), "commercial_lodging_requires_review")
                    .when(house & title.rlike(r"(?:bán\s+(?:gấp\s+)?(?:[0-9]+\s+)?lô\b|bán\s+đất\b)"), "land_listing_requires_review")
                    .otherwise("source_type_no_explicit_conflict"))
    out = out.withColumn("residential_scope_reason", scope_reason)
    out = out.withColumn("residential_scope_candidate", F.col("residential_scope_reason") == "source_type_no_explicit_conflict")
    # Remove formatting around numbers, preserving decimals and dimensions.
    area_text = F.regexp_replace(text, r"[*_]+", "")
    land_explicit = area_text.rlike(r"(?:diện tích đất(?: công nhận)?|dt đất|dtcn|diện tích công nhận|công nhận|\bcn)\s*[:=]?\s*[0-9]")
    floor_explicit = text.rlike(r"(?:tổng diện tích sàn|diện tích sàn|diện tích sử dụng)\s*[:=]?\s*[0-9]")
    number_pattern = r"(?:diện tích đất(?: công nhận)?|dt đất|dtcn|diện tích công nhận|công nhận|\bcn)\s*[:=]?\s*([0-9]+(?:[.,][0-9]+)?)\s*(?:m2|m²)"
    land_values = F.transform(F.regexp_extract_all(area_text, F.lit(number_pattern), 1),
                              lambda v: F.regexp_replace(v, ",", ".").cast("double"))
    land_number = F.element_at(land_values, 1)
    # Conflicting legal/land areas must not be hidden by the 5% numeric tolerance.
    land_conflict = F.size(F.array_distinct(land_values)) > 1
    valid_area = F.col("area").isNotNull() & ~F.isnan("area") & (F.col("area") > 0) & (F.col("area") < float("inf"))
    land_match = land_number.isNotNull() & ~land_conflict & (F.abs(land_number - F.col("area")) <= F.greatest(F.lit(1.0), F.col("area") * 0.05))
    out = out.withColumn("area_kind", F.when(apartment, "apartment")
                         .when(house & land_explicit & land_match, "land")
                         .when(house & floor_explicit & ~land_explicit, "floor")
                         .otherwise("unknown"))
    out = out.withColumn("area_evidence", F.when(~valid_area, "invalid_area")
                         .when(apartment, "property_type_only_requires_review")
                         .when(house & land_conflict, "conflicting_explicit_land_areas")
                         .when(house & land_match, "explicit_land_matches_area")
                         .when(house & land_explicit, "land_area_unmatched")
                         .when(house & floor_explicit, "floor_area_not_verified")
                         .otherwise("ambiguous_area"))
    def measure_matches(marker):
        pattern = marker + r"\s*[:=]?\s*([0-9]+(?:[.,][0-9]+)?)\s*(?:m2|m²)"
        number = F.regexp_replace(F.regexp_extract(area_text, pattern, 1), ",", ".").cast("double")
        return number.isNotNull() & (F.abs(number - F.col("area")) <= F.lit(0.1))
    net_matches, gross_matches = measure_matches("thông thủy"), measure_matches("tim tường")
    out = out.withColumn("area_measure", F.when(apartment & net_matches & ~gross_matches, "net")
                         .when(apartment & gross_matches & ~net_matches, "gross").otherwise("unspecified"))
    for key in ["province", "district", "ward"]:
        raw = F.trim(F.regexp_replace(F.lower(F.coalesce(F.col(key + "_name"), F.lit(""))), r"\s+", " "))
        if key == "district":
            raw = F.regexp_replace(raw, r"^(?:quận|huyện|q\.|h\.)\s*", "")
        if key == "ward":
            raw = F.regexp_replace(raw, r"^(?:phường|xã|p\.|x\.)\s*", "")
        out = out.withColumn(key + "_key", raw)
    out = out.withColumn("geo_key", F.concat_ws("|", "province_key", "district_key", "ward_key"))
    out = out.withColumn("geo_status", F.when(F.col("district_key") == "", "unresolved")
                         .when(F.col("ward_key") == "", "district_name_only")
                         .otherwise("ward_name_only_unmatched"))
    out = out.withColumn("published_ts", F.to_timestamp("published_at"))
    out = out.withColumn("published_month", F.date_format("published_ts", "yyyy-MM"))
    out = out.withColumn("unit_price_vnd", F.when(valid_area, F.col("price") / F.col("area")))
    # Retain raw addresses. This is a content fingerprint, not a verified property ID.
    out = out.withColumn("content_id", F.sha2(F.to_json(F.struct(*[F.col(c) for c in [
        "name", "description", "property_type_name", "province_name", "district_name", "ward_name", "area"
    ]]), options={"ignoreNullFields": "false"}), 256))
    out = out.withColumn("row_id", F.sha2(F.to_json(F.struct("content_id", "published_at", "price"), options={"ignoreNullFields": "false"}), 256))
    valid_price = F.col("price").isNotNull() & ~F.isnan("price") & (F.col("price") > 0) & (F.col("price") < float("inf"))
    eligibility = ((F.col("transaction_label") == "sale") & ~F.col("price_ambiguous")
                         & (apartment | house) & valid_price & valid_area & F.col("published_ts").isNotNull()
                         & (F.col("district_key") != "") & F.col("area_kind").isin("apartment", "land")
                         & F.col("residential_scope_candidate"))
    out = out.withColumn("candidate_eligible", F.coalesce(eligibility, F.lit(False)))
    return out
