import pandas as pd

make_to_country = {
    "Acura": "Japan",
    "Alfa Romeo": "Italy",
    "Audi": "Germany",
    "BMW": "Germany",
    "Buick": "USA",
    "Cadillac": "USA",
    "Chevrolet": "USA",
    "Chrysler": "USA",
    "Daihatsu": "Japan",
    "Dodge": "USA",
    "Eagle": "USA",
    "Ford": "USA",
    "Geo": "USA",
    "GMC": "USA",
    "Honda": "Japan",
    "Hyundai": "South Korea",
    "INFINITI": "Japan",
    "Isuzu": "Japan",
    "Jaguar": "UK",
    "Jeep": "USA",
    "Land Rover": "UK",
    "Lexus": "Japan",
    "Lincoln": "USA",
    "MAZDA": "Japan",
    "Mercedes-Benz": "Germany",
    "Mercury": "USA",
    "Mitsubishi": "Japan",
    "Nissan": "Japan",
    "Oldsmobile": "USA",
    "Plymouth": "USA",
    "Pontiac": "USA",
    "Porsche": "Germany",
    "Saab": "Sweden",
    "Saturn": "USA",
    "Subaru": "Japan",
    "Suzuki": "Japan",
    "Toyota": "Japan",
    "Volkswagen": "Germany",
    "Volvo": "Sweden",
    "HUMMER": "USA",
    "Kia": "South Korea",
    "Daewoo": "South Korea",
    "MINI": "UK",
    "Scion": "Japan",
    "Aston Martin": "UK",
    "Bentley": "UK",
    "Lotus": "UK",
    "Maserati": "Italy",
    "Maybach": "Germany",
    "Panoz": "USA",
    "Rolls-Royce": "UK",
    "Ferrari": "Italy",
    "Lamborghini": "Italy",
    "smart": "Germany",
    "Ram": "USA",
    "FIAT": "Italy",
    "Fisker": "USA",
    "McLaren": "UK",
    "Tesla": "USA",
    "Freightliner": "USA",
    "SRT": "USA",
    "Genesis": "South Korea",
    "Polestar": "Sweden",
    "Rivian": "USA",
    "Lucid": "USA",
    "VinFast": "Vietnam"
}

def get_country(make):
    return make_to_country.get(make, "Unknown")

df = pd.read_csv('combined_us_cars.csv')

df['country'] = df['make'].apply(get_country)

output_path = 'combined_us_cars_with_countries.csv'
df.to_csv(output_path, index=False)

print(f"Updated CSV file saved as {output_path}")
