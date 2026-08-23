import os
import sys
import subprocess

# Automatically detect Java path on Windows to avoid 'path not found' errors
if "JAVA_HOME" not in os.environ:
    try:
        java_path = subprocess.check_output(
            ["powershell", "-Command", "[System.Environment]::GetEnvironmentVariable('JAVA_HOME', 'Machine')"],
            text=True
        ).strip()
        if java_path:
            os.environ['JAVA_HOME'] = java_path
    except Exception:
        pass

if "JAVA_HOME" not in os.environ or not os.path.exists(os.environ['JAVA_HOME']):
    for p in [r"C:\Program Files\Java\jdk-17", r"C:\Program Files\Java\jdk-11", r"C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot"]:
        if os.path.exists(p):
            os.environ['JAVA_HOME'] = p
            break

os.environ['HADOOP_HOME'] = os.environ.get('JAVA_HOME', "")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count

def run_large_scale_pipeline():
    print("🚀 Initializing Large-Scale Spark Session...")
    
    # Create an optimized Spark session for large datasets
    spark = SparkSession.builder \
        .appName("Big Data E-Commerce Scale Pipeline") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    
    input_path = "./data/raw_large/*.parquet"
    print(f"📦 Reading large dataset from path: {input_path}")
    
    # Read parquet chunks in a distributed architecture
    df = spark.read.parquet(input_path)
    
    total_rows = df.count()
    print(f"✨ Total records loaded successfully: {total_rows:,}")
    
    print("\n--- Data Schema Overview ---")
    df.printSchema()
    
    # Perform large-scale grouping and aggregations by category and country
    print("\n📊 Running Distributed Calculations and Analytics...")
    analytics_summary = df.groupBy("category", "country").agg(
        _sum(col("price") * col("quantity")).alias("total_revenue"),
        count("user_id").alias("total_transactions"),
        avg("price").alias("avg_product_price")
    ).orderBy(col("total_revenue").desc())
    
    print("\nTop 10 Categories and Countries by Revenue Performance:")
    analytics_summary.show(10, truncate=False)
    
    # Save processed analytics data partitioned by category in Parquet format
    output_path = "./output_processed_analytics"
    print(f"\n💾 Saving partitioned analytics data to: {output_path}...")
    analytics_summary.write.mode("overwrite").partitionBy("category").parquet(output_path)
    
    print("\n🎉 Big Data Pipeline completed successfully from end to end!")
    spark.stop()

if __name__ == "__main__":
    run_large_scale_pipeline()