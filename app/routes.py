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

@routes.route("/graphs")
def graphs():
    try :
        print("Generating graphs...")
        images = [
            "repartition_cinemas_par_departement.png",
            "capacite_moyenne_sieges_par_multiplexe.png",
            "distribution_parts_marche_films_francais.png",
            "repartition_cinemas_par_tranche_entrees.png"
            ]
        print(images)
        return render_template("graphs.html", images=images)
    except Exception as e:
        print("error", e)
        return "Erreur lors de la génération des graphiques"

if __name__ == "__main__":
    app.run(debug=True)
