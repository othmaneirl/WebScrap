
# WebScrap

Ce dépôt contient les scripts et fichiers nécessaires pour effectuer le web scraping sur divers sites. Chaque répertoire est dédié à un site spécifique, contenant les scripts de scraping et les données extraites.

## Structure du dépôt

```
WebScrap/
│
├── .idea/
│
├── Airbnb_Final/
│   ├── Liens/
│   │   ├── Liens.csv
│   │   ├── LiensCorriges.csv
│   │   ├── LiensVilles.csv
│   │   ├── modifie_date_url.py
│   │   ├── urls.py
│   │   └── Liens.py
│   ├── ScrapingAirbnb.xlsx
│   ├── ExtractionInfos.py
│   └── instructions.txt
│
├── Avito/
│   ├── Liens/
│   │   ├── NumTelBoutiques.csv
│   │   ├── LiensBoutiquesArticles.csv
│   │   ├── Liens.csv
│   │   ├── LiensPagesBoutiques.py
│   │   ├── LiensAnnonces.py
│   │   └── LiensBoutiques.py
│   ├── ScrapingAvito.xlsx
│   ├── ExtractionInfos.py
│   └── instructions.txt
│
├── Charika.ma/
│   ├── Classements/
│   │   ├── classement.py
│   │   └── Classement2020.xlsx
│   ├── Liens/
│   │   ├── Liens.csv
│   │   └── Liens.py
│   ├── ScrapingCharika.xlsx
│   ├── collecte_infos.py
│   ├── collecte_infos_multi.py
│   ├── Nettoyage_dataset.py
│   └── instructions.txt
│
├── Kerix-export/
│   ├── Liens/
│   │   ├── Liens.csv
│   │   ├── EntreprisesParLettre.py
│   │   └── Liens.py
│   ├── ScrapingKerix-Export_final.xlsx
│   ├── ExtractionInfosKerix-export.py
│   └── instructions.txt
│
├── Kerix/
│   ├── Liens/
│   │   ├── Liens.csv
│   │   ├── EntreprisesParLettre.py
│   │   └── Liens.py
│   ├── ScrapingKerix.xlsx
│   ├── ExtractionInfosKerix.py
│   └── instructions.txt
│
├── LEI/
│   ├── Liens/
│   │   ├── Liens.csv
│   │   ├── Liens.py
│   │   └── traiterLiens.py
│   ├── ScrapingLEI.xlsx
│   ├── extraction_infos.py
│   └── instructions.txt
│
├── Mubawab/
│   ├── Liens/
│   │   ├── Liens_Loc_Vac.csv
│   │   ├── Liens_Loc.csv
│   │   ├── Liens_Ach.csv
│   │   └── urls.py
│   ├── ScrapingMubawab.xlsx
│   ├── extraction_infos.py
│   └── instructions.txt
│
├── Yakeey_Final/
│   ├── Liens/
│   │   ├── Liens.csv
│   │   └── Liens.py
│   ├── ScrapingYakeey.xlsx
│   ├── extraction_infos.py
│   └── instructions.txt
│
├── readme.md
└── requirements.txt
```

## Détails des répertoires

### .idea
Contient les fichiers de configuration pour le projet IDE.

### Airbnb_Final
Contient les scripts et données relatifs au scraping du site Airbnb.
- **Liens/**: Dossier contenant les fichiers `Liens.csv`, `LiensCorriges.csv`, `LiensVilles.csv`, `modifie_date_url.py`, `urls.py`, et `Liens.py`.
- **ScrapingAirbnb.xlsx**: Fichier Excel contenant les données extraites.
- **ExtractionInfos.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions. 
- Instructions: ordre d'execution des fichiers:
1-  urls.py
2-  Liens.py
3-  modifie_date_url.py  (seulement pour modifier dates de check in et check out des annonces)
4-  ExtractionsInfos.py

### Avito
Contient les scripts et données relatifs au scraping du site Avito.
- **Liens/**: Dossier contenant les fichiers `NumTelBoutiques.csv`, `LiensBoutiquesArticles.csv`, `Liens.csv`, `LiensPagesBoutiques.py`, `LiensAnnonces.py`, et `LiensBoutiques.py`.
- **ScrapingAvito.xlsx**: Fichier Excel contenant les données extraites.
- **ExtractionInfos.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: ordre d'execution des fichiers:
1-  LiensBoutiques.py
2-  LiensPagesBoutiques.py
3-  LiensAnnonces.py
4-  NumTelBoutiques.py
5-  Extraction infos.py

### Charika.ma
Contient les scripts et données relatifs au scraping du site Charika.ma.
- **Classements/**: Dossier contenant les fichiers `classement.py` et `Classement2020.xlsx`.
- **Liens/**: Dossier contenant les fichiers `Liens.csv` et `Liens.py`.
- **ScrapingCharika.xlsx**: Fichier Excel contenant les données extraites.
- **collecte_infos.py**: Script Python pour collecter les informations.
- **collecte_infos_multi.py**: Script Python pour collecter les informations multi-thread.
- **Nettoyage_dataset.py**: Script Python pour nettoyer les datasets.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: Pour extraction des données de toutes les sociétés:
1-  Executer "Liens.py" pour extraire les liens des sociétés
2-  Executer "collecte_infos_multi.py" pour extraire les données des sociétés avec un multiprocessing de 4
3-  Executer "Nettoyage_dataset.py" pour nettoyer les données

Pour extraction des classements des sociétés par année:
1- Executer "classement.py" en spécifiant l'année n
2- Executer "collecte_infos.py" pour extraire les données des 1000 premières sociétés marocaines de l'année n


### Kerix-export
Contient les scripts et données relatifs au scraping du site Kerix-export.
- **Liens/**: Dossier contenant les fichiers `Liens.csv`, `EntreprisesParLettre.py`, et `Liens.py`.
- **ScrapingKerix-Export_final.xlsx**: Fichier Excel contenant les données extraites.
- **ExtractionInfosKerix-export.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: 1- Executer EntreprisesParLettre.py
2- Executer Liens.py
3- Executer ExtractionInfosKerix-export.py


### Kerix
Contient les scripts et données relatifs au scraping du site Kerix.
- **Liens/**: Dossier contenant les fichiers `Liens.csv`, `EntreprisesParLettre.py`, et `Liens.py`.
- **ScrapingKerix.xlsx**: Fichier Excel contenant les données extraites.
- **ExtractionInfosKerix.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: 1- Executer EntreprisesParLettre.py
2- Executer Liens.py
3- Executer ExtractionInfosKerix.py


### LEI
Contient les scripts et données relatifs au scraping du site LEI.
- **Liens/**: Dossier contenant les fichiers `Liens.csv`, `Liens.py`, et `traiterLiens.py`.
- **ScrapingLEI.xlsx**: Fichier Excel contenant les données extraites.
- **extraction_infos.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: 1- Executer Liens.py
2- Executer traiterLiens.py
3- Executer extraction_infos.py

### Mubawab
Contient les scripts et données relatifs au scraping du site Mubawab.
- **Liens/**: Dossier contenant les fichiers `Liens_Loc_Vac.csv`, `Liens_Loc.csv`, `Liens_Ach.csv`, et `urls.py`.
- **ScrapingMubawab.xlsx**: Fichier Excel contenant les données extraites.
- **extraction_infos.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: 1- Executer 'urls.py'  en modifiant l'url de base a la ligne 25 et le nombre de pages maximum
2- Executer 'extraction_infos.py' pour extraire les informations des pages

### Yakeey_Final
Contient les scripts et données relatifs au scraping du site Yakeey.
- **Liens/**: Dossier contenant les fichiers `Liens.csv` et `Liens.py`.
- **ScrapingYakeey.xlsx**: Fichier Excel contenant les données extraites.
- **extraction_infos.py**: Script Python pour extraire les informations.
- **instructions.txt**: Fichier texte contenant les instructions.
- Instructions: 1- Executer Liens.py
2- Executer extraction_infos.py


## Installation

Pour installer les dépendances nécessaires, exécutez :

```bash
pip install -r requirements.txt
```

## Utilisation

Chaque répertoire contient des instructions spécifiques sur la façon d'exécuter les scripts de scraping. Référez-vous aux fichiers `instructions.txt` ou `README` présents dans chaque répertoire pour plus de détails.

## Contact

Pour toute question ou information supplémentaire, vous pouvez me contacter ici :


**IRHBOULA Othmane:**
- **Email**: oirhboula@gmail.com
- **Numéro de téléphone**: +33 6 22 09 12 47 / +212 7 08 57 92 20
- **LinkedIn**: [Profil LinkedIn](https://www.linkedin.com/in/othmane-irhboula/)
