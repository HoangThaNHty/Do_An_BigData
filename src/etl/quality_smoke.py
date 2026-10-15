"""Regression tests for material cross-field failures found during review."""
from src.config.spark import session
from src.etl.rules import enrich
from src.etl.quality import check


def main():
    spark = session("cross-field-quality-checks")
    try:
        cases = [
            ("Bán căn hộ 59m2 giá2tỷ850", "Diện tích59m2", "Căn hộ chung cư", "2850000000", 59., "advertised_price_matches", True),
            ("Bán căn hộ 88m2 giá3.85triệu", "Giá bán3.85triệu", "Căn hộ chung cư", "3850000000", 88., "advertised_price_conflict", False),
            ("Bán căn hộ 112m2 giá9.75tỷ", "Giá bán9.75tỷ", "Căn hộ chung cư", "9400000000", 112., "advertised_price_conflict", False),
            ("Bán căn hộ 46.8m2", "Giá tốt nhất thị trường", "Căn hộ chung cư", "7500000000", 46.8, "no_parseable_total_price", False),
            ("Mở bán dự án D-Homme", "40căn,diện tích dự án6000m2", "Căn hộ chung cư", "8000000000", 97., "no_parseable_total_price", False),
            ("Bán căn hộ giá900triệu", "Tổng giá900triệu", "Căn hộ chung cư", "900000000", 38., "advertised_price_matches", False),
            ("Bán nhà CN60m2giá8tỷ", "Đang cho thuê20triệu/tháng", "Nhà", "8000000000", 60., "advertised_price_matches", False),
            ("Bán căn hộ Officetel48m2giá3.79tỷ", "", "Căn hộ chung cư", "3790000000", 48., "advertised_price_matches", False),
            ("Bán căn hộ 70m2giá3tỷ85", "", "Căn hộ chung cư", "3850000000", 70., "ambiguous_price_format", False),
            ("Bán căn hộ 70m2giá3tỷ850", "Giá bán3tỷ850", "Căn hộ chung cư", "3850000000", 70., "advertised_price_matches", True),
            ("Bán căn hộ 70m2giá3tỷ", "Cho thuê12triệu/tháng,giá bán3tỷ", "Căn hộ chung cư", "3000000000", 70., "advertised_price_matches", True),
            ("Bán căn hộ70m2 giá bán từ6.5tỷ", "Căn70m2,giá bán từ6.5tỷ", "Căn hộ chung cư", "6500000000", 70., "advertised_price_matches", False),
            ("Căn2PN 78m2 với20.8TY số vốn", "Giỏ hàng bán căn78m2 26TY;20.8TY số vốn ban đầu", "Căn hộ chung cư", "20800000000", 78., "advertised_price_matches", False),
            ("Bán Tòa Building CN450m2 giá103tỷ", "Công nhận450m2,giá bán103tỷ", "Nhà", "103000000000", 450., "advertised_price_matches", False),
            ("Bán căn hộ70m2 giá3tỷ", "Booking100tr để nhận ưu đãi", "Căn hộ chung cư", "3000000000", 70., "advertised_price_matches", False),
            ("Bán nhà CN60m2giá8tỷ", "Hiện nhà ở chủ cải tạo thành CHDV", "Nhà", "8000000000", 60., "advertised_price_matches", False),
            ("Bán căn hộ70m2giá3tỷ", "Ngân hàng hỗ trợ vay80% tổng giá;giá bán3tỷ", "Căn hộ chung cư", "3000000000", 70., "advertised_price_matches", True),
            ("Bán nhà CN60m2 giá8tỷ 3PN", "Đang cho thuê20triệu/tháng, gia đình ở", "Nhà", "8000000000", 60., "advertised_price_matches", True),
            ("Bán nhà CN60m2 giá8tỷ", "Hiện trạng: Tòa nhà3tầng có phòng ngủ", "Nhà", "8000000000", 60., "advertised_price_matches", False),
            ("Bán nhà CN135m2 giá32tỷ 4PN", "Cần bán gấp BIỆT THỰ", "Nhà", "32000000000", 135., "advertised_price_matches", False),
            ("Bán căn hộ91m2 giá6tỷ3", "Giá6tỷ3–6.8tỷ", "Căn hộ chung cư", "6300000000", 91., "advertised_price_matches", False),
            ("Bán căn hộ97m2 giá7.8tỷ", "Trừ lại cho khách180triệu", "Căn hộ chung cư", "7800000000", 97., "advertised_price_matches", False),
            ("Bán căn hộ50m2 giá2.6tỷ", "Diện tích47m2, 2PN", "Căn hộ chung cư", "2600000000", 50., "advertised_price_matches", False),
            ("Bán căn hộ97m2 giá7.8tỷ", "Diện tích95m2, 2PN", "Căn hộ chung cư", "7800000000", 97., "advertised_price_matches", True),
            ("Bán căn hộ tháp A3 70m2 giá3tỷ", "Block A1, 2PN", "Căn hộ chung cư", "3000000000", 70., "advertised_price_matches", False),
            ("Bán studio26m2 giá2.95tỷ", "Loại officetel, đầy đủ nội thất", "Căn hộ chung cư", "2950000000", 26., "advertised_price_matches", False),
            ("Bán căn OT30m2 giá2.6tỷ", "Hoàn lại85tr cho khách nhận sổ", "Căn hộ chung cư", "2600000000", 30., "advertised_price_matches", False),
            ("Bán căn hộ80m2 giá6tỷ", "Đây là căn Văn phòng, kết hợp lưu trú", "Căn hộ chung cư", "6000000000", 80., "advertised_price_matches", False),
            ("Bán nhà CN126.8m2 giá9tỷ 4PN", "Ngang4m x dài13m, 4 phòng ngủ", "Nhà", "9000000000", 126.8, "advertised_price_matches", False),
            ("Bán duplex151m2 giá9.98tỷ", "Diện tích101 + lưng40m2 =151m2 4PN", "Căn hộ chung cư", "9980000000", 151., "advertised_price_matches", False),
            ("Bán nhà CN80m2 giá7.2tỷ", "Phù hợp xây mới hoặc cải tạo để ở", "Nhà", "7200000000", 80., "advertised_price_matches", False),
            ("Bán nhà CN52m2 giá7tỷ", "4mx13m, 3 phòng ngủ, ở ngay", "Nhà", "7000000000", 52., "advertised_price_matches", True),
        ]
        data = [(name, body, kind, price, area, "Hồ Chí Minh", "8", "5", "2025-06-01T05:00:00") for name, body, kind, price, area, *_ in cases]
        df = spark.createDataFrame(data, ["name", "description", "property_type_name", "price", "area", "province_name", "district_name", "ward_name", "published_at"])
        results = {(r.name, r.description):r for r in check(enrich(df)).collect()}
        for name, body, _, price, _, expected_check, expected_keep in cases:
            actual = results[(name, body)]
            assert actual.price_check == expected_check, actual
            assert actual.protected_candidate == expected_keep, actual
            assert actual.price_raw == price and actual.price == float(price), actual
            assert actual.validation_status == "provisional_requires_new_review"
        print(f"PASS: {len(cases)} cross-field cases; source prices retained; no clean-data claim.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
