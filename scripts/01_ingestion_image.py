import pandas as pd
import requests
import os
from PIL import Image
from io import BytesIO

# Charger listings
df = pd.read_csv("C:\\Users\\pcoko\\Les Etudes\\Année 4\\IABD\\Projet ImmoVision360\\ImmoVision360_DataLake\\data\\raw\\tabular\\listings.csv")

# garder seulement les lignes avec images
df = df[df["picture_url"].notna()]

# prendre un échantillon raisonnable
df = df.sample(2600, random_state=42)

# Dossier images
image_folder = "C:\\Users\\pcoko\\Les Etudes\\Année 4\\IABD\\Projet ImmoVision360\\ImmoVision360_DataLake\\data\\raw\\images"

os.makedirs(image_folder, exist_ok=True)

for index, row in df.iterrows():

    listing_id = row["id"]
    url = row["picture_url"]

    filename = f"{image_folder}/{listing_id}.jpg"

    # skip si existe
    if os.path.exists(filename):
        continue

    try:

        response = requests.get(url, timeout=10)

        if response.status_code == 200:

            img = Image.open(BytesIO(response.content))

            img = img.resize((320,320))

            img.save(filename)

            print(f"Downloaded {listing_id}")

    except:

        print(f"Error with {listing_id}")

