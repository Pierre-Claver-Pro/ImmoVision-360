README – Justification du choix d’extraction et méthodologie des données
Contexte métier

Le projet ImmoVision360 s’inscrit dans une démarche d’analyse de l’impact des locations de courte durée sur la transformation du marché immobilier parisien. L’objectif métier est d’identifier des signaux de gentrification à travers l’analyse des annonces Airbnb.

Trois hypothèses principales guident ce projet :

Hypothèse de standardisation : les logements deviennent des produits standardisés destinés au tourisme
Hypothèse de déshumanisation : la relation humaine disparaît au profit d’une gestion automatisée
Hypothèse de concentration économique : le marché est dominé par des investisseurs possédant plusieurs biens

Le choix des données extraites a été guidé par leur capacité à répondre à ces problématiques métier.

Justification du choix des variables (features)
Variables liées aux images (Computer Vision)

Afin de tester l’hypothèse de standardisation des logements, les variables suivantes ont été sélectionnées :

id : permet d’identifier chaque logement de manière unique
picture_url : permet de récupérer les images pour l’analyse visuelle
neighbourhood_cleansed : permet d’étudier les différences entre quartiers

Ces données permettront d’identifier des similarités visuelles entre logements pouvant indiquer une industrialisation du marché.

Variables liées aux textes (NLP)

Afin d’étudier la déshumanisation de l’expérience locative, les variables textuelles suivantes ont été extraites :

name
description
neighborhood_overview
host_about

Ces données permettront d’effectuer une analyse NLP afin de détecter :

un langage standardisé
la présence de termes liés à l’automatisation
la disparition du vocabulaire lié à l’accueil humain
Variables économiques (analyse du marché)

Pour analyser la dimension économique du marché :

price
availability_365
estimated_revenue_l365d
number_of_reviews

Ces variables permettent d’identifier si les logements sont exploités comme actifs financiers.

Variables liées aux propriétaires

Pour analyser la concentration du marché :

host_id
host_total_listings_count
calculated_host_listings_count

Ces variables permettent d’identifier les multi-propriétaires et les investisseurs professionnels.


```bash


Méthodologie d’extraction des données
Extraction des données tabulaires

Les données ont été extraites à partir du fichier listings.csv en utilisant la bibliothèque pandas.

import pandas as pd

df = pd.read_csv("../data/raw/tabular/listings.csv")

Cette étape permet de structurer les données pour les traitements futurs.

Exploration des données

Une exploration initiale a été réalisée afin d’identifier les colonnes pertinentes :

print(df.columns)

Cela a permis d’identifier les variables utiles pour les analyses futures.

Nettoyage des données

Afin d’assurer la qualité des données, les annonces ne contenant pas d’images ont été supprimées :



df = df[df["picture_url"].notna()]

Cela permet d’éviter les erreurs lors de l’ingestion des images.

Réduction des données (logique métier et technique)

Afin d’optimiser les performances et éviter une surcharge de stockage, un échantillon représentatif de 2600 annonces a été sélectionné :

df = df.sample(2600, random_state=42)

Ce choix répond à deux objectifs :

Objectif technique :
réduire le temps de téléchargement
limiter l’utilisation mémoire
améliorer les performances
Objectif métier :
conserver un échantillon représentatif
permettre une analyse statistique fiable
éviter les biais liés à une sélection séquentielle
Ingestion des images

Un script Python a été développé pour automatiser le téléchargement des images.

Pour chaque annonce :

récupération de l'id
récupération de l’URL image
téléchargement via requests
redimensionnement des images
sauvegarde locale

Exemple :
'
response = requests.get(url, timeout=10)
img = Image.open(BytesIO(response.content))
img = img.resize((320,320))
Standardisation des images

Les images ont été redimensionnées en 320x320 pixels afin de :

Objectif technique :

standardiser les données
faciliter le traitement ML
réduire la taille mémoire

Objectif métier :

permettre une comparaison visuelle cohérente
améliorer la détection de similarités
Stockage des données

Les images ont été stockées dans :

data/raw/images

Chaque image est nommée avec l’identifiant du logement :

filename = f"{listing_id}.jpg"

Cela permet de maintenir le lien entre les données tabulaires et les images.

Robustesse du pipeline

Afin d’assurer la fiabilité du processus :

gestion des erreurs réseau
vérification des fichiers existants
timeout sur requêtes

Exemple :

try:
    response = requests.get(url, timeout=10)
except:
    print("Download error")


Conclusion

La méthodologie d’extraction mise en place permet de construire un dataset cohérent répondant aux objectifs métier du projet. Cette approche garantit l’alignement entre les données collectées, les hypothèses analytiques et les futures analyses en data science.