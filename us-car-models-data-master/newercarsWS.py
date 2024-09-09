import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_msrp_cars(make, model, year):

    make_formatted = make.lower().replace(' ', '_')
    model_formatted = model.lower().replace(' ', '_')
    year_formatted = str(year)
    
    class_name = "msrp spark-heading-3 "
    
    if re.match('^[0-9]+$', model_formatted):
        url = f"https://www.cars.com/research/{make_formatted}-{year_formatted}/"
    else:
        url = f"https://www.cars.com/research/{make_formatted}-{model_formatted}-{year_formatted}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        msrp_element = soup.find(attrs={"class": class_name})
        
        if msrp_element:
            try:
                msrp = msrp_element.get_text().strip().replace('$', '').replace(',', '')
                msrp_value = float(msrp)
                return msrp_value
            except ValueError:
                return "MSRP not found"
        
        return "MSRP not found"
    
    else:
        return "Page not found"

input_path = 'combined_with_msrp.csv'
df = pd.read_csv(input_path)

for index, row in df.iterrows():
    if row['year'] > 2022:
        df.at[index, 'starting_msrp'] = scrape_msrp_cars(row['make'], row['model'], row['year'])

df.to_csv(input_path, index=False)

print(f"Updated CSV file saved as {input_path}")