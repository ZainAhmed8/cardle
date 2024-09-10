import pandas as pd

df = pd.read_csv('combined_us_cars.csv')

unique_makes = df['make'].unique()
print('unique car makes:')
for make in unique_makes:
    print(make)