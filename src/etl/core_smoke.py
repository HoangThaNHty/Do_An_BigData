"""Material regressions for geography and temporal repost leakage."""
from pyspark.sql import functions as F
from src.config.spark import session
from src.etl.geography import attach, key
from src.etl.core import reposts, temporal


def main():
    assert key("Phường 02") == "2" and key("Thành phố Thủ Đức") == "thủ đức"
    spark = session("geo-repost-regression")
    try:
        schema = "source_record_id string, name string, description string, property_type_name string, district_name string, ward_name string, area double, published_at string"
        rows = [
            ("a","Bán căn hộ 70m2 giá3tỷ","Căn số A12,giá bán3tỷ","Căn hộ chung cư","Quận 2","Phường An Phú",70.,"2025-11-01"),
            ("b","Bán căn hộ 70m2 giá4tỷ","Căn số A12,giá bán4tỷ","Căn hộ chung cư","Quận 2","Phường An Phú",70.,"2026-01-01"),
            ("c","Bán căn hộ 70m2 giá4tỷ","Căn số B19,giá bán4tỷ","Căn hộ chung cư","Quận 2","Phường An Phú",70.,"2026-01-01"),
            ("d","Bán nhà","Địa chỉ mới ngoài phạm vi","Nhà","Vũng Tàu","Phước Thắng",70.,"2026-01-01"),
        ]
        frame = spark.createDataFrame(rows,schema).withColumn("published_ts",F.to_timestamp("published_at")).withColumn("published_month",F.date_format("published_ts","yyyy-MM"))
        joined = attach(frame,spark)
        mapped = {r.source_record_id:r for r in joined.collect()}
        assert mapped['a'].district_code == '769' and mapped['a'].ward_code is not None
        assert mapped['d'].district_code is None and mapped['d'].geo_match_status == 'district_outside_or_unresolved'
        groups = temporal(reposts(joined.where("district_code IS NOT NULL")))
        records = {r.source_record_id:r for r in groups.collect()}
        assert records['a'].repost_group == records['b'].repost_group != records['c'].repost_group
        assert records['a'].repost_rank == 1 and records['b'].repost_rank == 2
        kept = groups.where("repost_rank=1").collect()
        assert {r.source_record_id for r in kept} == {'a','c'}
        assert records['a'].split == 'train' and records['c'].split == 'test'
        print('PASS: qualified district+ward joins, outside-scope geography, price-revised repost, temporal retention')
    finally:
        spark.stop()


if __name__ == '__main__':
    main()
