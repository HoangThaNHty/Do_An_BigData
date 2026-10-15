import os
from pathlib import Path
from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[2]


def session(name):
    temp = ROOT / ".runtime/spark-tmp"
    temp.mkdir(parents=True, exist_ok=True)
    builder = (SparkSession.builder.appName(name)
             .master(os.environ.get("SPARK_MASTER", "local[4]"))
             .config("spark.local.dir", str(temp))
             .config("spark.sql.shuffle.partitions", "16")
             .config("spark.sql.adaptive.enabled", "true")
             .config("spark.sql.session.timeZone", "Asia/Ho_Chi_Minh")
             .config("spark.ui.showConsoleProgress", "false"))
    if os.name == "nt":
        adapter = ROOT / ".runtime/project-local-fs.jar"
        if not adapter.exists():
            raise RuntimeError("Build Windows local filesystem adapter using scripts/build_local_fs.ps1")
        builder = (builder.config("spark.driver.extraClassPath", str(adapter))
                   .config("spark.executor.extraClassPath", str(adapter))
                   .config("spark.hadoop.fs.file.impl", "vn.huit.realestate.ProjectLocalFileSystem"))
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
