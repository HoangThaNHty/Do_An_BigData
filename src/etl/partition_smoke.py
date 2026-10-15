"""Regression for Windows local partition directory names and commits."""
from src.config.spark import ROOT, session


def main():
    spark = session("partition-filesystem-regression")
    try:
        rows = [(1, "Nhà", "2025-06"), (2, "Căn hộ chung cư", "2025-07"),
                (3, "Nhà", None), (4, "Căn hộ chung cư", "2025-06")]
        frame = spark.createDataFrame(rows, "id int, property_type string, month string")
        target = str(ROOT / ".runtime/partition-regression/listings")
        for _ in range(2):
            frame.write.mode("overwrite").partitionBy("property_type", "month").parquet(target)
            actual = {tuple(row) for row in spark.read.parquet(target).select("id", "property_type", "month").collect()}
            assert actual == set(rows), actual
        fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(spark._jsc.hadoopConfiguration())
        statuses = fs.listStatus(spark._jvm.org.apache.hadoop.fs.Path(target))
        assert all(status.getPath().getName() for status in statuses)
        print("PASS: partition commits, Unicode names, null partition and overwrite")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
