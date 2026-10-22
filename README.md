# stabilite-reseau-electrique
# Prédire la stabilité d'un réseau électrique avant de modifier son réglage

Projet final S7MOI1 · Science des données · ECAM-EPMI · 2AE
Auteure : Mame Diarra Sock

## Problème et résultat

Un gestionnaire de réseau électrique simule chaque réglage avant de l'appliquer (0,5 h par simulation, 20 000 réglages par an). Nous testons un modèle utilisé comme **pré-filtre** : un réglage jugé stable est appliqué directement, les autres passent par la simulation.

- **Cible** : `stabf` (stable / instable), classification binaire, classe positive = instable.
- **Modèle retenu** : Random Forest (PR-AUC 0,984 en validation croisée, contre 0,638 pour la baseline et 0,960 pour la régression logistique).
- **Seuil** : choisi par les coûts sur les probabilités hors pli de l'entraînement (0,12 lors de la dernière exécution présentée dans le rapport) : recall 100 %, precision 76,6 %, 16,7 % de simulations évitées.
- **Valeur** : environ 100 000 € par an de simulations évitées, avant coût des incidents. Les coûts (30 € par simulation, 2 000 € par incident) sont des **hypothèses**, pas des mesures.
- **Limite** : données simulées sur un réseau simplifié à 4 nœuds ; recommandation de pilote avant tout déploiement.

Le détail figure dans le rapport de synthèse (`reports/`).

## Structure

```
├── README.md
├── requirements.txt
├── data/        # Data_for_UCI_named.csv
├── notebooks/
│   ├── 01_cadrage_eda.ipynb
│   ├── 02_modelisation.ipynb
│   └── 03_decision_roi.ipynb
├── src/         # utils.py : chargement, variables, seuils et coûts
└── reports/     # rapport PDF, probabilités et modèle enregistrés
```

## Lancer le projet

```
git clone https://github.com/diarrsock-create/stabilite-reseau-electrique
cd stabilite-reseau-electrique
pip install -r requirements.txt
jupyter notebook
```

Exécuter les notebooks **dans l'ordre 01, 02, 03** avec « Restart & Run All ». Le notebook 02 écrit dans `reports/` les probabilités que le notebook 03 relit. `random_state=42` et chemins relatifs.

## Données

Electrical Grid Stability Simulated Data, UCI Machine Learning Repository (id 471), copie Kaggle : https://www.kaggle.com/datasets/ishadss/electrical-grid-stability-simulated-data-dataset

## Déclaration d'usage de l'IA générative

Outil : Claude (Anthropic), utilisé comme assistant pour structurer le projet et la note de cadrage, configurer Git et l'environnement Python, et produire une première version des notebooks, relue, testée et complétée par l'étudiante.
