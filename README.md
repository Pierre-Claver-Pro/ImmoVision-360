# ImmoVision 360 – Data Lake Creation

## 1. Contexte du projet

L'objectif de ce projet est de construire un Data Lake multimodal pour ImmoVision360 afin de préparer les données pour des analyses futures en NLP et Computer Vision.

Le Data Lake contient :

- Données tabulaires (listings)
- Images des annonces
- Textes des reviews

Les données sont filtrées sur le périmètre **Élysée**.

---

## 2. Structure du projet

Structure du repository :

ImmoVision360_DataLake/

│

├── data/

│   ├── raw/

│   │   ├── images/

│   │   ├── texts/

│   │   ├── tabular/

│   │       ├── listings.csv
│   │       ├── reviews.csv

│

├── scripts/

│   ├── 01_ingestion_image.py
│   ├── 02_ingestion_textes.py
│   ├── 03_sanity_check.py

│

├── README.md

├── 00_data.ipynb

---

## 3. Instructions d'exécution

Installer les librairies nécessaires :

```bash
pip install pandas requests pillow

4. Audit des données

Résultats du sanity check :

Listings de référence : 2625

Images :

Images attendues : 2625
Images présentes : (mettre ton résultat)
Taux de complétion : (mettre ton %)

Textes :

Textes attendus : 2625
Textes présents : 1965
Taux de complétion : 74.86 %

Incohérences :

Images sans texte : 2450
Textes sans image : 1903
5. Analyse des pertes de données

La différence entre les données attendues et obtenues peut s'expliquer par :

URLs d'images expirées
Images supprimées par Airbnb
Erreurs réseau
Protection anti scraping
Listings sans reviews

Ces pertes sont normales dans un pipeline de data ingestion réel.

6. Conclusion

Le Data Lake a été construit avec succès.

Les trois pipelines permettent :

ingestion images
ingestion textes
validation qualité

Les données sont maintenant prêtes pour :

NLP
Computer Vision
Machine Learning