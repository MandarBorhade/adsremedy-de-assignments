import os
import logging
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, lower, initcap, upper, regexp_replace, to_date, 
    when, current_date, months_between, floor, concat_ws, split
)
from pyspark.sql.types import DoubleType

# Configure logging
# Configure logging to file inside the work-dir
log_dir = "/opt/spark/work-dir/scripts/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_dir, "data_cleaning.log"),
    filemode='a'
)
logger = logging.getLogger(__name__)

spark = None

try:
    # SPARK SESSION
    spark = (
        SparkSession.builder.master("spark://spark-master:7077")
        .appName("EmployeeDataCleaning")
        .config("spark.sql.session.timeZone", "Asia/Kolkata")
        .getOrCreate()
    )

    logger.info("Spark session started. Loading data...")

    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_pattern = os.path.join(base_dir, "data", "employees_*.csv")
    output_folder = os.path.join(base_dir, "data", "cleaned_output")

    # 1. Load Data
    df = spark.read.csv(input_pattern, header=True, inferSchema=True)
    logger.info(f"Data loaded. Processing {df.count()} raw records.")

    # dropping nulls and removing duplicates
    exclude_cols = ["manager_id"]
    include_cols = [c for c in df.columns if c not in exclude_cols]
    df_clean = df.dropna(subset=include_cols)

    # handling inconsistent values
    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    df_clean = df_clean.filter(col("email").rlike(email_regex))

    df_clean = (
        df_clean.withColumn("first_name", initcap(trim(col("first_name"))))
        .withColumn("last_name", initcap(trim(col("last_name"))))
        .withColumn("email", lower(trim(col("email"))))
        .withColumn("job_title", initcap(trim("job_title")))
        .withColumn("department", upper(trim(col("department"))))
        .withColumn("status", upper(trim(col("status"))))
        .withColumn("hire_date", to_date("hire_date", "yyyy-MM-dd"))
        .withColumn("birth_date", to_date("birth_date", "yyyy-MM-dd"))
        .withColumn("salary", regexp_replace(col("salary"), "[$,]", "").cast("int"))
        .withColumn("manager_id", when(col("manager_id") == "N/A", None).otherwise(col("manager_id")))
    )

    df_clean = df_clean.drop_duplicates(["employee_id"]).drop_duplicates(["email"])

    # Hiring date validation
    df_clean = df_clean.filter((col("hire_date") < current_date()) | (col("hire_date") < col("birth_date")))

    # Adding age, tenure and salary band
    df_transformed = df_clean.withColumn("age", floor(months_between(current_date(), col("birth_date")) / 12))
    df_transformed = df_transformed.withColumn("tenure_years", floor(months_between(current_date(), col("hire_date")) / 12))
    df_transformed = df_transformed.withColumn(
        "salary_band",
        when(col("salary") < 50000, "JUNIOR")
        .when((col("salary") >= 50000) & (col("salary") < 80000), "MID")
        .otherwise("SENIOR")
    )

    # Adding full name and email domain
    df_enriched = df_transformed.withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name")))\
                                .withColumn("email_domain", split(col("email"), "@").getItem(1))

    # Final dataset selection
    df_final = df_enriched.select(
        "employee_id", "first_name", "last_name", "full_name", "email", "email_domain", "hire_date", 
        "job_title", "department", "salary", "salary_band", "manager_id", "address", "city", 
        "state", "zip_code", "birth_date", "age", "tenure_years", "status"
    )

    # 6. Save Output
    logger.info(f"Saving cleaned data to {output_folder}")
    df_final.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_folder)
    logger.info("Data cleaning completed successfully.")

except Exception as e:
    logger.error(f"Error during data cleaning: {str(e)}", exc_info=True)
    raise
finally:
    if spark:
        spark.stop()