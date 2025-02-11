import joblib
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

model = joblib.load("models/random_forest_model.pkl")

def generate_interactive_plot(min_entrees, max_entrees, fauteuils=300, restrictions=50):
    # Générer les taux de reprise entre 0.1 et 1.0
    taux_reprise_values = np.linspace(0.1, 1.0, 10)

    # Générer les valeurs d'entrées attendues entre min et max
    entrees_intervals = np.linspace(min_entrees, max_entrees, 10)

    traces = []

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

    # Créer le layout
    layout = go.Layout(
        title="Simulation des entrées en fonction du taux de reprise",
        xaxis=dict(title="Taux de reprise"),
        yaxis=dict(title="Nombre d'entrées prédites"),
        hovermode="closest",
        legend=dict(title="Entrées attendues"),
    )

    fig = go.Figure(data=traces, layout=layout)
    # Générer le graphique HTML à intégrer dans la page Flask
    return pio.to_html(fig, full_html=False)
