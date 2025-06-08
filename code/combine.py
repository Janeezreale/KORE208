import os
import pandas as pd

base_dir = 'topics'

for subfolder in os.listdir(base_dir):
    subfolder_path = os.path.join(base_dir, subfolder)
    
    if os.path.isdir(subfolder_path):
        combined_df = pd.DataFrame()
        
        for filename in os.listdir(subfolder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(subfolder_path, filename)
                
                if os.path.getsize(file_path) == 0:
                    continue
                
                try:
                    df = pd.read_csv(file_path)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        output_file = os.path.join(base_dir, f"{subfolder}.csv")
        combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Combined CSV file saved to: {output_file}")
