import pandas as pd
import os
import numpy as np
import google.generativeai as genai
from PIL import Image

# ==============================
# CONFIG API
# ==============================

genai.configure(api_key="AIzaSyCAqhrj5hwiqknWPPbeypxzTIh1JJIBO6o")

model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("../data/raw/tabular/listings.csv")

print("DATASET SHAPE :",df.shape)

# ==============================
# DATA PROFILING
# ==============================

print("\nPRICE PROFILING")
print(df["price"].describe())

print("\nNAN FEATURES")
print(df.isna().sum())

print("\nCATEGORICAL FEATURES")
print(df.select_dtypes(include="object").columns)

# ==============================
# CLEAN PRICE
# ==============================

df["price"] = df["price"].replace("$","",regex=True)

df["price"] = df["price"].replace(",","",regex=True)

df["price"] = pd.to_numeric(df["price"],errors="coerce")

# detect price outliers

df["price_outlier"] = df["price"] > 1000

# ==============================
# FILTER VALID IMAGES
# ==============================

df = df[df["picture_url"].notna()]

# TEST SAMPLE FIRST (important)
df = df.sample(50,random_state=42)

# ==============================
# IMAGE CLASSIFICATION
# ==============================

results = []

prompt = """
Analyse cette image Airbnb.

Classe STRICTEMENT dans UNE catégorie :

Industrialized :
Appartement type hôtel, décor standard, minimaliste.

Non-industrialized :
Appartement personnel, décor vécu, objets personnels.

Irrelevant :
Image ne montrant pas un logement intérieur
(exemple : pont, rue, restaurant, monument).

Répond uniquement par :

Industrialized
Non-industrialized
Irrelevant
"""

for index,row in df.iterrows():

    listing_id = row["id"]

    image_path = f"../data/raw/images/{listing_id}.jpg"

    if os.path.exists(image_path):

        try:

            img = Image.open(image_path)

            response = model.generate_content([prompt,img])

            category = response.text.strip()

            print(listing_id,category)

            results.append(category)

        except:

            results.append("Error")

    else:

        results.append("Missing")

# ==============================
# CREATE FEATURES
# ==============================

df["Standardization_Score"] = results

df["image_irrelevant"] = df["Standardization_Score"] == "Irrelevant"

df["industrialized"] = df["Standardization_Score"] == "Industrialized"

# ==============================
# SAVE DATASET
# ==============================

os.makedirs("../data/processed",exist_ok=True)

df.to_csv("../data/processed/transformed_elysee.csv",index=False)

print("\nTRANSFORMATION DONE")