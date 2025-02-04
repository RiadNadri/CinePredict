import joblib
import pandas as pd

def predict_future_entries(model_file, input_data):
    # Chargement du modèle
    model = joblib.load(model_file)

    # Données simulées
    new_data = pd.DataFrame(input_data, columns=['fauteuils','entrées 2019', 'duree_fermeture', 'restrictions', 'taux_reprise'])

    # Prédictions
    predictions = model.predict(new_data)
    print(f"Prédictions des entrées futures : {predictions}")

    # Sauvegarde des résultats
    new_data['Prédictions pandémie'] = predictions
    new_data.to_csv("../data/predictions/predictions.csv", index=False)

if __name__ == "__main__":
    # Exemple de données futures
    future_data = [
        [510, 145188, 4, 20, 0.8],  # 300 fauteuils, forte fermeture, restrictions élevées, faible reprise
        [150, 15000, 3, 50, 0.7]   # Restrictions moyennes, bonne reprise
    ]    
    predict_future_entries("../models/random_forest_model.pkl", future_data)
