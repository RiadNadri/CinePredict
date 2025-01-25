# Define routes for the Flask app
from flask import Blueprint, Flask, render_template
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier `.env`
load_dotenv()

# Récupérer le chemin du fichier CSV depuis les variables d'environnement
file__path = os.getenv("CINEMA_CSV_PATH")

routes = Blueprint("routes", __name__, template_folder="templates")

app = Flask(__name__, template_folder="app/templates")

# Charger les données
df = pd.read_csv(file__path, sep=";")

# Route pour la page d'accueil


@routes.route("/")
def index():
    return render_template("index.html")

# Route pour afficher les graphiques


@routes.route("/dashboard")
def graphs():
    try:
        print("Generating graphs...")
        graphs = [
            {"title": "Répartition des cinémas par département",
                "image": "repartition_cinemas_par_departement.png", "details": "details_1"},
            {"title": "Répartition des entrées totales par département",
                "image": "repartition_entrees_par_departement.png", "details": "details_2"},
            {"title": "Comparaison des entrées 2019 vs 2020",
                "image": "comparaison_entrees_2019_2020.png", "details": "details_3"},
            {"title": "Performances des cinémas (fauteuils vs entrées 2020)",
             "image": "performances_fauteuils_vs_entrees_2020.png", "details": "details_4"},
            {"title": "Répartition des cinémas par tranche d'entrées annuelles",
                "image": "repartition_cinemas_par_tranche_entrees.png", "details": "details_5"}

        ]
        return render_template("dashboard.html", graphs=graphs)
    except Exception as e:
        print("error", e)
        return "Erreur lors de la génération des graphiques"


if __name__ == "__main__":
    app.run(debug=True)
