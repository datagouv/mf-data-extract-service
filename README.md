# Extraction de données PNT Meteo-France (Prévision Numérique du Temps)

Ce script permet de télécharger de manière régulière les batches de runs de modèles Arpege, Arome, Arome Outre-Mer et Vague et Surcote de Météo-France.

## Principe

Plusieurs étapes sont réalisés par ce script :
- Remove and create local data folder # Créer un dossier local pour le téléchargement des données
- Get latest theorical batches # Récupère les runs théoriques précédents (configurer pour récupérer les 3 derniers runs)
- Construct all possibles files # A partir des runs théoriques, construire tous les URLs possibles et ne garder que celles dont les données n'ont pas déjà été téléchargées
- Processing each possible files # Télécharge la donnée en local puis la push sur Minio
- Publish all new files in data.gouv.fr # Publication sur data.gouv.fr de la ressource (en mode remote)
- Reorder resources of data.gouv for each dataset # Reorder des ressources des jeux de données
- Remove files in minio and data.gouv.fr if more than MAX BATCH SIZE # Supprimer les anciens batches minio dépassant une certaine date (plus d'un jour).
- Delete local data folder # Suppression du répertoire local

## Pré-requis

Les tokens pour chacun des modèles sont à récupérés sur [le portail API de Météo-France](https://portail-api.meteofrance.fr/web/). Par défaut, un rate limiting est appliqué (50req/s).

## Installation

Remplir le fichier d'environnement `.env` comme suit : 

```
MINIO_URL="127.0.0.1:9000"
MINIO_PUBLIC_URL="object.data.gouv.fr"
MINIO_BUCKET="meteofrance-pnt"
MINIO_USER="USER"
MINIO_PASSWORD="PASSWORD"
MINIO_SECURE="False" # ou "True"

APIKEY_DATAGOUV="API KEY"
APIKEY_ARPEGE="API KEY"
APIKEY_AROME="API KEY"
APIKEY_AROME_OM="API KEY"
APIKEY_VAGUE_SURCOTE="API KEY"
```

Installer les dépendances

```
python -m venv mf
source mf/bin/activate
pip install -r requirements.txt
```

## Run

```
python process_pnt.py arome
python process_pnt.py arpege
python process_pnt.py arome-om
python process_pnt.py vague-surcote
```


