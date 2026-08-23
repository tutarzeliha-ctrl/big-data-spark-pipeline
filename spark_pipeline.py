import os
os.environ['JAVA_HOME'] = r"C:\Users\ZELİHA TUTAR\AppData\Local\Programs\Eclipse Adoptium\jdk-11.0.32.9-hotspot"
os.environ['PATH'] = os.path.join(os.environ['JAVA_HOME'], 'bin') + ";" + os.environ.get('PATH', '')

import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count

def run_spark_pipeline():
    print("🚀 Initializing Spark Session...")
    
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("E-Commerce Retention & Big Data Pipeline") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    
    print("📦 Loading and processing data...")
    
    # Create sample e-commerce dataset for testing
    data = [
        ("101", "Electronics", 1200.0, 1),
        ("102", "Clothing", 150.0, 2),
        ("103", "Electronics", 800.0, 1),
        ("104", "Home", 300.0, 3),
        ("105", "Clothing", 250.0, 1),
        ("106", "Home", 450.0, 2)
    ]
    
    columns = ["order_id", "category", "amount", "customer_id"]
    df = spark.createDataFrame(data, columns)
    
    print("\n--- Raw Data Preview ---")
    df.show()
    
    # Perform category-based aggregations
    print("\n📊 Running Category Analytics...")
    category_summary = df.groupBy("category").agg(
        _sum("amount").alias("total_revenue"),
        count("order_id").alias("order_count"),
        avg("amount").alias("avg_order_value")
    )
    
    category_summary.show()
    
    # Save data partitioned by category in Parquet format
    output_path = "./output_partitioned_data"
    print(f"\n💾 Saving partitioned data to {output_path}...")
    df.write.mode("overwrite").partitionBy("category").parquet(output_path)
    
    print("\n✨ Spark Pipeline executed successfully!")
    spark.stop()

if __name__ == "__main__":
    run_spark_pipeline()