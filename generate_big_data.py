import os
import numpy as np
import pandas as pd

# Configuration for Large Scale Data Generation
NUM_ROWS = 100_000
CHUNK_SIZE = 25_000
BRONZE_PATH = "output_bronze"

os.makedirs(BRONZE_PATH, exist_ok=True)

print("🚀 Generating raw e-commerce data for Bronze layer...")

categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]
countries = ["USA", "DE", "TR", "UK", "FR"]

for i in range(0, NUM_ROWS, CHUNK_SIZE):
    chunk_df = pd.DataFrame({
        "transaction_id": range(i, i + CHUNK_SIZE),
        "category": np.random.choice(categories, CHUNK_SIZE),
        "country": np.random.choice(countries, CHUNK_SIZE),
        "product_price": np.random.uniform(10.0, 500.0, CHUNK_SIZE),
        "quantity": np.random.randint(1, 5, CHUNK_SIZE),
        "timestamp": pd.date_range(start="2026-01-01", periods=CHUNK_SIZE, freq="s")
    })
    
    # Calculate raw total amount
    chunk_df["total_amount"] = chunk_df["product_price"] * chunk_df["quantity"]
    
    # Save as chunked Parquet files into Bronze layer
    file_path = os.path.join(BRONZE_PATH, f"raw_data_chunk_{i}.parquet")
    chunk_df.to_parquet(file_path, index=False)
    print(f"📦 Saved Bronze chunk: {file_path}")

print("✅ Bronze layer data generation completed successfully!")