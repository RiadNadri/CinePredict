import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score

def evaluate_model(model_file, X_test_file, y_test_file):
    model = joblib.load(model_file)
    # data = pd.read_csv(data_file)

    X_test = pd.read_csv(X_test_file)
    y_test = pd.read_csv(y_test_file)

    # Prédictions
    y_pred = model.predict(X_test)

    # Calcul des métriques
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MAE : {mae}")
    print(f"R² : {r2}")

if __name__ == "__main__":
    evaluate_model("../models/random_forest_model.pkl",  "../data/test/X_test.csv", "../data/test/Y_test.csv")
