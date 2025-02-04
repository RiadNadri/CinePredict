import joblib
import pandas as pd

def predict_future_entries(model_file, input_data):
    # Chargement du modèle
    model = joblib.load(model_file)

    # Données simulées (exemple)
    new_data = pd.DataFrame(input_data, columns=['fauteuils', 'Multiplexe', 'entrées 2019'])

    # Prédictions
    predictions = model.predict(new_data)
    print(f"Prédictions des entrées futures : {predictions}")

    # Sauvegarde des résultats
    new_data['Prédictions 2025'] = predictions
    new_data.to_csv("../data/predictions/predictions.csv", index=False)

if __name__ == "__main__":
    # Exemple de données futures
    future_data = [[300, 1, 20000], [150, 0, 20000]]
    predict_future_entries("../models/random_forest_model.pkl", future_data)
