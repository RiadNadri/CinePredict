from scripts.preprocess import preprocess_data
from scripts.train_model import train_model
from scripts.evaluate_model import evaluate_model
from scripts.predict import simulate_reprise
import os as os

if __name__ == "__main__":

    cinema_file = os.getenv("CINEMA_CSV_PATH")

    # Étape 1 : Prétraitement des données
    preprocess_data(cinema_file, "data/processed/cinemas_cleaned.csv")

    # Étape 2 : Entraînement du modèle
    train_model("data/processed/cinemas_cleaned.csv", "models/random_forest_model.pkl")

    # Étape 3 : Évaluation du modèle
    # evaluate_model("models/random_forest_model.pkl", "data/test/X_test.csv", "data/test/Y_test.csv")

    # Étape 4 : Génération des prédictions futures
    # future_data = [[300, 1, 20000], [150, 0, 15000]]  # Exemple
    # predict_future_entries("models/random_forest_model.pkl", future_data)
    simulate_reprise(30000, 70000, "models/random_forest_model.pkl",fauteuils=300, restrictions=50)
