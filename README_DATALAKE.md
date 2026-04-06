Présentation
Ce Data Lake centralise les données brutes issues d'Airbnb pour le quartier Élysée (Paris).
Il constitue la première couche du pipeline ETL du projet ImmoVision360, avant transformation et chargement dans le Data Warehouse PostgreSQL.


Table principale : elysee_tabular
ColonneTypeDescriptionidbigintIdentifiant unique de l'annoncecalculated_host_listings_countintegerNombre d'annonces du même hôteavailability_365smallintJours de disponibilité sur l'année (0–365)host_response_rate_numnumeric(6,2)Taux de réponse de l'hôte (0–100 %)room_type_codesmallintType de logement (voir mapping)host_response_time_codesmallintDélai de réponse (voir mapping)standardization_scoresmallintProfil visuel de l'annonce (-1 / 0 / 1)neighborhood_impact_scoresmallintImpact sur le voisinage (-1 / 0 / 1)
Mappings des codes
room_type_code
CodeSignification0Shared room (chambre partagée)1Private room (chambre privée)2Entire home/apt (logement entier)3Hotel room-1Inconnu
host_response_time_code
CodeSignification0Dans l'heure1En quelques heures2Dans la journée3Plusieurs jours ou plus-1Inconnu
standardization_score
ScoreSignification1Appartement industrialisé (style catalogue)0Appartement personnel (vécu)-1Non classable / erreur
neighborhood_impact_score
ScoreSignification1Hôtélisé (peu de lien humain)0Voisinage naturel (vie de quartier)-1Ambigu / texte absent / erreur

Installation & Import
Prérequis

PostgreSQL 18 installé et démarré
psql accessible dans le PATH
Base immovision créée

Créer la base (une seule fois)
sqlCREATE DATABASE immovision;
Importer les données
cmdcd DataWarehouse/sql/postgres
psql -U postgres -d immovision -f import_elysee_tabular.sql
Vérifier l'import
cmdpsql -U postgres -d immovision -c "SELECT COUNT(*) FROM elysee_tabular;"
-- Résultat attendu : 2625 lignes

Pipeline ETL
Données brutes Airbnb (raw/)
        ↓
   Filtrage Élysée
        ↓
  Encodage & nettoyage
  (room_type → code, etc.)
        ↓
  elysee_tabular.csv (processed/)
        ↓
  Import PostgreSQL → table elysee_tabular
        ↓
  Analyse EDA (EDA.ipynb)

Analyse exploratoire (EDA)
L'analyse est réalisée dans le notebook EDA.ipynb et répond aux 3 questions de la Mairie :

Le quartier Élysée est-il en train de devenir un quartier fantôme ?
→ availability_365, room_type_code
Quel est le profil des hôtes ? Particuliers ou professionnels ?
→ calculated_host_listings_count, host_response_rate_num, host_response_time_code
Quel est l'impact sur le voisinage et le "vivre-ensemble" ?
→ neighborhood_impact_score, standardization_score


Technologies utilisées
OutilUsagePostgreSQL 18Stockage relationnelPython / PandasAnalyse et visualisationJupyter NotebookEDA interactiveMatplotlib / SeabornGraphiquespsqlImport SQL en ligne de commande