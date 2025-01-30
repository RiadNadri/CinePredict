# Define routes for the Flask app
from flask import Blueprint, Flask, render_template
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier `.env`
load_dotenv()

# Récupérer le chemin du fichier CSV depuis les variables d'environnement
# file__path = os.getenv("CINEMA_CSV_PATH")

routes = Blueprint("routes", __name__, template_folder="templates")

app = Flask(__name__, template_folder="app/templates")

# Charger les données
# df = pd.read_csv(file__path, sep=";")

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
                "image": "repartition_cinemas_par_departement.png", "details": "Paris (75) domine avec le plus grand nombre de cinémas. Cela reflète la concentration culturelle et démographique de la capitale."},
            {"title": "Répartition des entrées totales par département",
                "image": "repartition_entrees_par_departement.png", "details": "Les entrées sont majoritairement concentrées à Paris (75), représentant plus de 7M d'entrées en 2020."},
            {"title": "Comparaison des entrées 2019 vs 2020",
                "image": "comparaison_entrees_2019_2020.png", "details": "La pandémie a entraîné une chute des entrées en 2020, avec une majorité des cinémas en dessous de leurs performances 2019."},
            {"title": "Performances des cinémas (fauteuils vs entrées 2020)",
             "image": "performances_fauteuils_vs_entrees_2020.png", "details": "Les cinémas avec un grand nombre de fauteuils ont tendance à enregistrer plus d'entrées, bien que des exceptions existent."},
            {"title": "Répartition des cinémas par tranche d'entrées annuelles",
                "image": "repartition_cinemas_par_tranche_entrees.png", "details": "La majorité des cinémas se situent dans les tranches de 5 000 à 20 000 entrées, reflétant une forte proportion de petites salles."}

        ]
        return render_template("dashboard.html", graphs=graphs)
    except Exception as e:
        print("error", e)
        return "Erreur lors de la génération des graphiques"


if __name__ == "__main__":
    app.run(debug=True)
