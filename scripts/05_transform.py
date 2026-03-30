import pandas as pd
import os
import numpy as np

print("Starting transform phase...")

# Charger données extract
df = pd.read_csv("data/processed/filtered_elysee.csv")

print(f"Initial shape: {df.shape}")

# =========================
# NETTOYAGE
# =========================

# Price float
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Host response rate
if "host_response_rate" in df.columns:
    df["host_response_rate"] = pd.to_numeric(
        df["host_response_rate"],
        errors="coerce"
    )

# Reviews
if "reviews_per_month" in df.columns:
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

if "review_scores_rating" in df.columns:
    df["review_scores_rating"] = df["review_scores_rating"].fillna(
        df["review_scores_rating"].median()
    )

# Response time missing
if "host_response_time" in df.columns:
    df["host_response_time"] = df["host_response_time"].fillna("unknown")

# =========================
# OUTLIERS PRICE
# =========================

df = df[df["price"] > 10]
df = df[df["price"] < 5000]

# =========================
# FEATURES ECONOMIC
# =========================

# Multi property host
df["multi_property_host"] = (
    df["calculated_host_listings_count"] > 3
).astype(int)

# Commercial usage
df["commercial_usage"] = (
    df["availability_365"] > 200
).astype(int)

# =========================
# FEATURES SOCIAL
# =========================

df["professional_host"] = (
    df["host_response_rate"] > 90
).astype(int)

# =========================
# FEATURES QUALITY
# =========================

df["high_rating"] = (
    df["review_scores_rating"] > 4.5
).astype(int)

# =========================
# IA FEATURES (mock safe)
# =========================

def fake_image_score():
    return np.random.randint(0,3)

def fake_text_score():
    return np.random.randint(0,2)

# Standardization score
df["Standardization_Score"] = df["id"].apply(
    lambda x: fake_image_score()
)

# Neighborhood impact
df["Neighborhood_Impact"] = df["id"].apply(
    lambda x: fake_text_score()
)

# =========================
# SAVE
# =========================

os.makedirs("data/processed", exist_ok=True)

output = "data/processed/transformed_elysee.csv"

df.to_csv(output,index=False)

print("Transform completed")
print(f"Final shape: {df.shape}")
print(f"Saved: {output}")