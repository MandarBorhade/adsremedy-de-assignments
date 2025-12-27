from pyspark.sql import SparkSession
import os
import logging

# 1. Setup specific log directory and file path
log_dir = "/opt/spark/work-dir/scripts/logs"
log_file = os.path.join(log_dir, "load_to_postgres.log")
os.makedirs(log_dir, exist_ok=True)

# 2. Configure Logger with a FileHandler to ensure it writes to the volume
logger = logging.getLogger("LoadToPostgres")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if script is re-run in same session
if not logger.handlers:
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

spark = None

try:
    logger.info("Initializing Spark Session for Postgres Load...")
    spark = (
        SparkSession.builder.master("spark://172.19.0.3:7077")
        .appName("LoadToPostgres")
        .config("spark.sql.session.timeZone", "Asia/Kolkata")
        .getOrCreate()
    )

    # 1. Read the cleaned data
    input_path = "/opt/spark/work-dir/scripts/data/cleaned_output"
    logger.info(f"Reading data from {input_path}")
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # 2. Database Connection
    db_url = "jdbc:postgresql://postgres-db:5432/adsremedy"
    properties = {
        "user": "myuser",
        "password": "mypassword",
        "driver": "org.postgresql.Driver",
        "truncate": "True",
    }

    # 3. Write to Postgres
    logger.info(f"Attempting to write {df.count()} records to dev.employees_clean...")
    df.write.jdbc(
        url=db_url, table="dev.employees_clean", mode="overwrite", properties=properties
    )

    logger.info("Data successfully loaded to Postgres!")

except Exception as e:
    logger.error(f"Critical error during Postgres load: {str(e)}", exc_info=True)
    raise
finally:
    if spark:
        logger.info("Stopping Spark Session.")
        spark.stop()