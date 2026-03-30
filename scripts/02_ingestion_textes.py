import pandas as pd
import os
import re

listings_path = "C:\\Users\\pcoko\\Les Etudes\\Année 4\\IABD\\Projet ImmoVision360\\ImmoVision360_DataLake\\data\\raw\\tabular\\listings.csv"
reviews_path = "C:\\Users\\pcoko\\Les Etudes\\Année 4\\IABD\\Projet ImmoVision360\\ImmoVision360_DataLake\\data\\raw\\tabular\\reviews.csv"
output_folder = "C:\\Users\\pcoko\\Les Etudes\\Année 4\\IABD\\Projet ImmoVision360\\ImmoVision360_DataLake\\data\\raw\\texts"

os.makedirs(output_folder, exist_ok=True)

print("Loading listings...")

listings = pd.read_csv(listings_path)

# vérifier le vrai nom colonne
elysee_listings = listings[
    listings["neighbourhood_cleansed"].str.contains("Élysée", na=False)
]

valid_ids = set(elysee_listings["id"])

print(f"{len(valid_ids)} listings Elysee")

print("Loading reviews...")

reviews = pd.read_csv(reviews_path)

# garder seulement les reviews utiles
reviews = reviews[reviews["listing_id"].isin(valid_ids)]

def clean_text(text):

    if pd.isna(text):
        return ""

    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\n+", " ", text)

    return text.strip()

print("Grouping reviews...")

grouped = reviews.groupby("listing_id")["comments"].apply(list)

print("Writing files...")

for listing_id, comments in grouped.items():

    filename = f"{output_folder}/{listing_id}.txt"

    if os.path.exists(filename):
        continue

    try:

        with open(filename, "w", encoding="utf-8") as f:

            f.write(f"Commentaires pour l'annonce {listing_id}:\n\n")

            for comment in comments:

                clean_comment = clean_text(comment)

                if clean_comment:
                    f.write(f"- {clean_comment}\n")

        print(f"Created {listing_id}")

    except Exception as e:

        print(f"Error {listing_id}: {e}")

print("Done")