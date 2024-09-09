import os
import pandas as pd

directory = os.getcwd()

dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

output_path = os.path.join(directory, 'combined_us_cars.csv')
combined_df.to_csv(output_path, index=False)

print(f"Combined CSV file saved as {output_path}")