import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape MSRP from Cars.com
def scrape_msrp_cars(make, model, year):
    # Replace spaces with underscores
    make_formatted = make.lower().replace(' ', '_').replace('-', '_')
    model_formatted = model.lower().replace(' ', '_')
    year_formatted = str(year)
    
    url = f"https://www.cars.com/research/{make_formatted}-{model_formatted}-{year_formatted}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        msrp_element = soup.find(attrs={"class": "spark-heading-4"}) # try to add a new class for new cars (2023/2024) "msrp spark-heading-3 "

        if msrp_element is None:
            msrp_element = soup.find(attrs={"class": "msrp spark-heading-3 "})
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

file_path = 'combined_us_cars_with_countries.csv'

df = pd.read_csv(file_path)

df['starting_msrp'] = df.apply(lambda row: scrape_msrp_cars(row['make'], row['model'], row['year']), axis=1)
# otpt = scrape_msrp_cars('Acura', 'NSX', '1992')

output_path = 'combined_with_msrp.csv'
df.to_csv(output_path, index=False)

print(f"Updated CSV file saved as {output_path}")
# print(otpt)
