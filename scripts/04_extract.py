import pandas as pd
import os

print("Starting extract phase...")

# 1 — Chargement
df = pd.read_csv("data/raw/tabular/listings.csv")

print(f"Initial dataset shape: {df.shape}")

# 2 — Colonnes sélectionnées selon hypothèses métier

COLS_TO_KEEP = [

    # ================= ECONOMIC HYPOTHESIS =================
    # détecter concentration immobilière
    "id",  # identifiant unique → traçabilité
    "price",  # prix du logement → analyse économique
    "property_type",  # type de bien → marché immobilier
    "room_type",  # type location → modèle business
    "availability_365",  # niveau exploitation → usage commercial
    "calculated_host_listings_count",  # détecte multipropriété

    # ================= SOCIAL HYPOTHESIS =================
    # professionnalisation des hosts

    "host_response_time",  # rapidité réponse → automatisation
    "host_response_rate",  # taux réponse → professionnalisation

    # ================= REVIEW ACTIVITY =================
    # activité logement

    "number_of_reviews",  # popularité logement
    "review_scores_rating",  # qualité perçue
    "reviews_per_month",  # activité commerciale

    # ================= LOCATION =================
    # filtrage géographique

    "neighbourhood_cleansed",  # filtrage Elysee
    "latitude",  # localisation GPS
    "longitude"  # localisation GPS

]



# garder seulement colonnes existantes
existing_cols = [col for col in COLS_TO_KEEP if col in df.columns]

df = df[existing_cols]

print(f"After column selection: {df.shape}")

# 3 — Filtrage Elysee

df = df[
    df["neighbourhood_cleansed"].str.contains("Élysée", na=False)
]

print(f"After Elysee filter: {df.shape}")

# 4 — Nettoyage price

if "price" in df.columns:

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("$","", regex=False)
        .str.replace(",","", regex=False)
        .astype(float)
    )

# 5 — Nettoyage response rate

if "host_response_rate" in df.columns:

    df["host_response_rate"] = (
        df["host_response_rate"]
        .astype(str)
        .str.replace("%","", regex=False)
    )

# 6 — Créer dossier processed

os.makedirs("data/processed", exist_ok=True)

# 7 — Sauvegarde

output_path = "data/processed/filtered_elysee.csv"

df.to_csv(output_path, index=False)

print("Extract completed")
print(f"Saved: {output_path}")
print(f"Final shape: {df.shape}")