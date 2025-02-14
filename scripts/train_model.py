import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import joblib

def train_model(data_file, model_output):
    # Chargement des données nettoyées
    data = pd.read_csv(data_file)

    # Sélection des features et de la cible
    X = data[['fauteuils', 'entrées 2019', 'taux_reprise_historique', 'restrictions']]
    y = data['entrées 2020']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraînement Random Forest Regressor
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    # model = XGBRegressor(n_estimators=100, max_depth=10, learning_rate=0.1)
    model.fit(X_train, y_train)

    X_test.to_csv("../data/test/X_test.csv", index=False)
    y_test.to_csv("../data/test/Y_test.csv", index=False)

    # Sauvegarde du modèle
    joblib.dump(model, model_output)
    print("Modèle entraîné et sauvegardé.")

if __name__ == "__main__":
    train_model("../data/processed/cinemas_cleaned.csv", "../models/random_forest_model.pkl")
