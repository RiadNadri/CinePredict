import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio


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


def simulate_reprise(min_entrees, max_entrees, model_file, fauteuils=300, restrictions=50):

    # Chargement du modèle
    model = joblib.load(model_file)
    # Générer des taux de reprise entre 0.1 et 1.0
    taux_reprise_values = np.linspace(0.05, 0.2, 10)

    # Générer un intervalle d'entrées attendu
    entrees_intervals = np.linspace(min_entrees, max_entrees, 10)
    predictions = []

    # Calculer les prédictions pour chaque combinaison (taux de reprise et entrées)
    for entrees in entrees_intervals:
        scenario_predictions = []
        for taux_reprise in taux_reprise_values:
            input_data = np.array([[fauteuils, entrees, taux_reprise, restrictions]])
            prediction = model.predict(input_data)[0]
            scenario_predictions.append(prediction)
        predictions.append(scenario_predictions)

    # Générer un graphique
    plt.figure(figsize=(10, 6))
    for i, entrees in enumerate(entrees_intervals):
        plt.plot(taux_reprise_values, predictions[i], label=f"Entrées attendues: {int(entrees)}")

    plt.xlabel("Taux de reprise")
    plt.ylabel("Nombre d'entrées prédits")
    plt.title("Simulation des entrées en fonction du taux de reprise et des attentes")
    plt.legend()
    plt.grid(True)
    plt.show()


def generate_interactive_plot(model_file, min_entrees, max_entrees, fauteuils, restrictions):
    model = joblib.load(model_file)

    # Générer les taux de reprise entre 0.1 et 1.0
    taux_reprise_values = np.linspace(0.05, 0.5, 40)

    # Générer les valeurs d'entrées attendues entre min et max
    entrees_intervals = np.linspace(min_entrees, max_entrees, 20)

    traces = []
    conseils = []

    # Calcul des prédictions pour chaque combinaison
    for entrees in entrees_intervals:
        predictions = [
            model.predict(np.array([[fauteuils, entrees, taux, restrictions]]))[0] for taux in taux_reprise_values
        ]

        # Ajouter une trace pour chaque courbe d'entrées attendues
        trace = go.Scatter(
            x=taux_reprise_values,
            y=predictions,
            mode='lines+markers',
            name=f"Attentes: {int(entrees)}",
            text=[f"Attentes: {int(entrees)}<br>Prédiction: {int(prediction)}<br>Taux de reprise: {taux:.2f}"
                  for prediction, taux in zip(predictions, taux_reprise_values)],
            hoverinfo='text'
        )
        traces.append(trace)

        # Ajouter des conseils basés sur les prédictions
        if max(predictions) > 50000:
            conseils.append(f"Pour des attentes de {int(entrees)}, les prédictions sont élevées. Considérez d'augmenter les capacités.")
        elif min(predictions) < 10000:
            conseils.append(f"Pour des attentes de {int(entrees)}, les prédictions sont faibles. Réduisez les coûts ou améliorez les stratégies de marketing.")
        else:
            conseils.append(f"Pour des attentes de {int(entrees)}, les prédictions sont moyennes. Maintenez les opérations actuelles.")

    # Créer le layout et afficher le graphique
    layout = go.Layout(
        title="Simulation des entrées en fonction du taux de reprise",
        xaxis=dict(title="Taux de reprise"),
        yaxis=dict(title="Nombre d'entrées prédites"),
        hovermode="closest",
        legend=dict(title="Entrées attendues"),
    )

    fig = go.Figure(data=traces, layout=layout)
    plot_html = pio.to_html(fig, full_html=False)

    # Retourner le graphique et les conseils
    return plot_html, conseils


if __name__ == "__main__":
    # Exemple de données futures
    # future_data = [
    #     [510, 145188, 4, 20, 0.8],  # 300 fauteuils, forte fermeture, restrictions élevées, faible reprise
    #     [150, 15000, 3, 50, 0.7]   # Restrictions moyennes, bonne reprise
    # ]    
    # predict_future_entries("../models/random_forest_model.pkl", future_data)
    # simulate_reprise(30000, 70000, "../models/random_forest_model.pkl", fauteuils=300, restrictions=50)
    generate_interactive_plot("../models/random_forest_model.pkl", 30000, 70000, )