# Cinema Prediction Application 
Description of the project. 


### REQUIREMENTS

To install all packages : 

pip install -r requirements.txt



## 📂 Structure du projet
- **data/** : Contient les datasets bruts, nettoyés et les prédictions.
- **notebooks/** : Analyses exploratoires.
- **models/** : Modèles sauvegardés.
- **scripts/** : Scripts Python pour le pipeline de traitement.

## Fonctionnalités principales
- Nettoyage et prétraitement des données.
- Entraînement des modèles.
- Génération des prédictions futures.

## HEROKU DEPLOYEMENT

git push heroku main  

heroku open

## Création d'environnement virtuel

python -m venv venv

Pour Linux : 

source venv/bin/activate

Pour Windows : 
venv\Scripts\activate



### Preprocessing

python scripts/preprocess.py

### Model Training

python scripts/train_model.py


### Model test

python scripts/evaluate_model.py


### Predictions 

python scripts/predict.py


