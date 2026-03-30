import pandas as pd
import os

print("Loading listings...")

listings = pd.read_csv("data/raw/tabular/listings.csv")

# filtrage Elysee (adapter si colonne différente)
elysee = listings[
    listings["neighbourhood_cleansed"].str.contains("Élysée", na=False)
]

valid_ids = set(elysee["id"])

print(f"Reference listings: {len(valid_ids)}")

# dossiers
image_folder = "data/raw/images"
text_folder = "data/raw/texts"

# fichiers physiques
image_files = {
    int(f.replace(".jpg",""))
    for f in os.listdir(image_folder)
    if f.endswith(".jpg")
}

text_files = {
    int(f.replace(".txt",""))
    for f in os.listdir(text_folder)
    if f.endswith(".txt")
}

# comptages images
expected_images = len(valid_ids)
actual_images = len(image_files)

missing_images = valid_ids - image_files
orphan_images = image_files - valid_ids

# comptages textes
expected_texts = len(valid_ids)
actual_texts = len(text_files)

missing_texts = valid_ids - text_files
orphan_texts = text_files - valid_ids

# cohérence croisée
image_no_text = image_files - text_files
text_no_image = text_files - image_files

print("\n===== SANITY CHECK REPORT =====\n")

print("Perimetre Elysee:")
print(f"Listings reference: {len(valid_ids)}")

print("\nIMAGES")
print(f"Expected: {expected_images}")
print(f"Present: {actual_images}")

completion = (actual_images / expected_images) * 100

print(f"Completion: {completion:.2f}%")

print(f"Missing images: {len(missing_images)}")

print("First missing IDs:")
print(list(missing_images)[:5])

print("\nTEXTS")

print(f"Expected: {expected_texts}")
print(f"Present: {actual_texts}")

completion = (actual_texts / expected_texts) * 100

print(f"Completion: {completion:.2f}%")

print(f"Missing texts: {len(missing_texts)}")

print("First missing IDs:")
print(list(missing_texts)[:5])

print("\nCROSS CHECK")

print(f"Images without text: {len(image_no_text)}")
print(list(image_no_text)[:5])

print(f"Texts without image: {len(text_no_image)}")
print(list(text_no_image)[:5])

print("\nDone.")