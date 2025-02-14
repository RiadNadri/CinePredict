import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

def generate_interactive_plot(model_file, min_entrees, max_entrees, fauteuils, restrictions):
    model = joblib.load(model_file)

    taux_reprise_values = np.linspace(0.1, 1.0, 40)

    entrees_intervals = np.linspace(min_entrees, max_entrees, 20)

    traces = []

    for entrees in entrees_intervals:
        predictions = [
            model.predict(np.array([[fauteuils, entrees, taux, restrictions]]))[0] for taux in taux_reprise_values
        ]

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

    layout = go.Layout(
        title="Simulation des entrées en fonction du taux de reprise",
        xaxis=dict(title="Taux de reprise"),
        yaxis=dict(title="Nombre d'entrées prédites"),
        hovermode="closest",
        legend=dict(title="Entrées attendues"),
    )

    fig = go.Figure(data=traces, layout=layout)
    # fig.show()
    plot_html = pio.to_html(fig, full_html=False)

    return plot_html


if __name__ == "__main__":
    generate_interactive_plot(
        "../models/random_forest_model.pkl", 30000, 70000, fauteuils=3642, restrictions=50)
