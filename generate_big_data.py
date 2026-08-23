import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_large_dataset(num_rows=2_000_000, chunk_size=500_000):
    """
    Simulates millions of e-commerce / clickstream records 
    and saves them in optimized parquet chunks to manage memory.
    """
    print(f"🚀 Starting generation of {num_rows:,} rows of big data...")
    
    output_dir = "data/raw_large"
    os.makedirs(output_dir, exist_ok=True)
    
    categories = ['Electronics', 'Apparel', 'Home & Kitchen', 'Books', 'Sports']
    countries = ['TR', 'US', 'DE', 'GB', 'NL', 'FR']
    devices = ['Mobile', 'Desktop', 'Tablet']
    
    start_date = datetime(2025, 1, 1)
    
    chunks_written = 0
    for i in range(0, num_rows, chunk_size):
        current_chunk_size = min(chunk_size, num_rows - i)
        
        # Vectorized data generation for speed
        user_ids = np.random.randint(10000, 99999, size=current_chunk_size)
        product_ids = np.random.randint(100, 5000, size=current_chunk_size)
        category_col = np.random.choice(categories, size=current_chunk_size)
        price_col = np.round(np.random.uniform(5.0, 1500.0, size=current_chunk_size), 2)
        quantity_col = np.random.choice([1, 2, 3, 4, 5], size=current_chunk_size, p=[0.7, 0.2, 0.05, 0.03, 0.02])
        country_col = np.random.choice(countries, size=current_chunk_size, p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05])
        device_col = np.random.choice(devices, size=current_chunk_size, p=[0.6, 0.3, 0.1])
        
        # Random timestamps within the last year
        random_seconds = np.random.randint(0, 31536000, size=current_chunk_size)
        timestamps = [start_date + timedelta(seconds=int(sec)) for sec in random_seconds]
        
        df_chunk = pd.DataFrame({
            'user_id': user_ids,
            'product_id': product_ids,
            'category': category_col,
            'price': price_col,
            'quantity': quantity_col,
            'country': country_col,
            'device': device_col,
            'event_timestamp': timestamps
        })
        
        # Extract partition columns (Year and Month) for optimization later
        df_chunk['year'] = df_chunk['event_timestamp'].dt.year
        df_chunk['month'] = df_chunk['event_timestamp'].dt.month
        
        # Save chunk as Parquet
        chunk_path = os.path.join(output_dir, f"part_{chunks_written}.parquet")
        df_chunk.to_parquet(chunk_path, index=False)
        
        chunks_written += 1
        print(f"📦 Chunk {chunks_written} ({current_chunk_size:,} rows) written to disk.")

    print(f"✅ Data generation complete! Total rows: {num_rows:,}. Saved in '{output_dir}'.")

if __name__ == "__main__":
    generate_large_dataset()