"""Regression checks for material sale/rental and area ambiguities."""
from src.config.spark import session
from src.etl.rules import enrich


def main():
    spark = session("rules-regression-check")
    try:
        cases = [
            ("Bán căn hộ 70m2 giá 3 tỷ", "", "Căn hộ chung cư", 3e9, 70., "sale", "apartment", True),
            ("Cho thuê căn hộ 70m2", "12 triệu/tháng", "Căn hộ chung cư", 12e6, 70., "rent", "apartment", False),
            ("Bán nhà 8 tỷ", "Đang cho thuê 20 triệu/tháng. Diện tích đất 60m2", "Nhà", 8e9, 60., "sale", "land", True),
            ("Bán hoặc cho thuê căn hộ", "", "Căn hộ chung cư", 3e9, 70., "uncertain", "apartment", False),
            ("Bán căn hộ chỉ cần trả trước 500 triệu", "", "Căn hộ chung cư", 5e8, 70., "sale", "apartment", False),
            ("Bán nhà 60m2 3 tầng", "", "Nhà", 5e9, 60., "sale", "unknown", False),
            ("Bán nhà diện tích đất 90m2", "", "Nhà", 5e9, 60., "sale", "unknown", False),
            ("Cần mua căn hộ", "", "Căn hộ chung cư", 3e9, 70., "uncertain", "apartment", False),
            ("Bán tòa nhà", "Đang cho thuê 300 triệu/tháng. Diện tích đất công nhận: 501,1m². Giá bán 95 tỷ", "Nhà", 95e9, 501., "sale", "land", False),
            ("Bán CH Cantavil", "Nhận kí gửi cho thuê. Diện tích 77m2", "Căn hộ chung cư", 3e9, 77., "sale", "apartment", True),
            ("Bán căn hộ Officetel", "40m2 giá 2.6 tỷ", "Căn hộ chung cư", 2.6e9, 40., "sale", "apartment", False),
            ("Bán biệt thự", "CN 278m2", "Nhà", 21e9, 278., "sale", "land", False),
            ("Bán nhà sổ công nhận 40m2", "Diện tích 60m2", "Nhà", 6e9, 60., "sale", "unknown", False),
            ("Nhà Thạch Lam", "Thích hợp kinh doanh hoặc cho thuê", "Nhà", 5e9, 40., "uncertain", "unknown", False),
            ("Gấp bán giá 2tỷ1, nhà cho thuê dòng tiền", "Diện tích đất 47.2m2. Đang cho thuê 23 triệu/tháng", "Nhà", 2.1e9, 47.2, "sale", "land", True),
            ("Bán căn hộ giá vô hạn", "", "Căn hộ chung cư", float("inf"), 70., "sale", "apartment", False),
            ("Bán căn hộ diện tích vô hạn", "", "Căn hộ chung cư", 3e9, float("inf"), "sale", "apartment", False),
            ("Bán nhà CN180m2", "DTCN173m2", "Nhà", 19e9, 180., "sale", "unknown", False),
            ("Bán khách sạn", "Giá bán550tỷ. CN1125m2", "Nhà", 550e9, 1125., "sale", "land", False),
            ("Bán căn hộ diện tích70m2", "Thông thủy67m2", "Căn hộ chung cư", 3.3e9, 70., "sale", "apartment", True),
            ("Nhà riêng bán tại Bình Hưng Hòa", "", "Nhà", 3e9, 30., "sale", "unknown", False),
            ("Chính chủ cần bán gấp-Nhà", "CN53m2", "Nhà", 9.2e9, 53., "sale", "land", True),
            ("Bán Cantavil Premier", "Nhận ký gửi, bán - cho thuê BĐS", "Căn hộ chung cư", 9.4e9, 111., "sale", "apartment", True),
            ("Căn hộ Riviera", "Đang có hợp đồng thuê18tr/tháng", "Căn hộ chung cư", 7.5e9, 92., "uncertain", "apartment", False),
            ("Khu vực kinh doanh mua bán sầm uất", "", "Nhà", 6e9, 28., "uncertain", "unknown", False),
            ("Không bán căn hộ", "", "Căn hộ chung cư", 3e9, 70., "uncertain", "apartment", False),
            ("Bán nhà đang cho thuê22tr", "Nhà còn hợp cho thuê22triệu/tháng. CN68.6m2", "Nhà", 3.5e9, 68.6, "sale", "land", True),
        ]
        records = [(a,b,c,d,e,"Hồ Chí Minh","8","5","2025-06-01T05:00:00") for a,b,c,d,e,*_ in cases]
        df = spark.createDataFrame(records, ["name", "description", "property_type_name", "price", "area", "province_name", "district_name", "ward_name", "published_at"])
        result = {r.name:r for r in enrich(df).collect()}
        for name,_,_,_,_,label,area,eligible in cases:
            actual = result[name]
            assert (actual.transaction_label, actual.area_kind, actual.candidate_eligible) == (label,area,eligible), actual
        assert result["Bán căn hộ diện tích70m2"].area_measure == "unspecified"
        # Actual source schema has string prices; retain prices above int32 max.
        from pyspark.sql import functions as F
        string_result = {r.name:r for r in enrich(df.withColumn("price", F.col("price").cast("string"))).collect()}
        for name,_,_,price,_,label,area,eligible in cases:
            actual = string_result[name]
            assert actual.price == price, actual
            assert (actual.transaction_label, actual.area_kind, actual.candidate_eligible) == (label,area,eligible), actual
        # Verify parquet IO too; this catches Windows Hadoop native IO problems early.
        from src.config.spark import ROOT
        target = ROOT / ".runtime/smoke-parquet"
        spark.range(8).write.mode("overwrite").parquet(str(target))
        assert spark.read.parquet(str(target)).count() == 8
        spark.range(5).write.mode("overwrite").parquet(str(target))
        assert spark.read.parquet(str(target)).count() == 5
        from pyspark.ml.feature import VectorAssembler
        from pyspark.ml.regression import LinearRegression, LinearRegressionModel
        from pyspark.sql import functions as F
        toy = spark.range(20).withColumn("x", F.col("id").cast("double")).withColumn("label", F.col("x") * 2 + 1)
        toy = VectorAssembler(inputCols=["x"], outputCol="features").transform(toy)
        model = LinearRegression(regParam=0.01).fit(toy)
        saved = ROOT / ".runtime/smoke-model"
        model.write().overwrite().save(str(saved))
        loaded = LinearRegressionModel.load(str(saved))
        assert loaded.transform(toy).count() == 20
        assert abs(loaded.coefficients[0] - model.coefficients[0]) < 1e-10
        print(f"PASS: {len(cases)} context checks (numeric/string prices), Parquet IO/overwrite, MLlib fit/save/reload.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
