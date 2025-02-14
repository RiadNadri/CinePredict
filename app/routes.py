from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
import joblib
# from app.model import generate_interactive_plot  # Assurez-vous que le chemin est correct
from scripts.predict import generate_interactive_plot

routes = Blueprint("routes", __name__, template_folder="templates")

app = Flask(__name__, template_folder="app/templates")
app.secret_key = "secret_key"  # Clé secrète pour les messages flash

def load_cinema_data():
    file_path = "data/raw/les_salles_de_cinemas_en_ile-de-france.csv"
    df = pd.read_csv(file_path, sep=";", encoding="ISO-8859-1")

    # Nettoyage des données
    df.columns = df.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)
    df.iloc[:, 1] = df.iloc[:, 1].astype(str).str.strip()  # 2ème colonne pour les départements
    df['nom'] = df['nom'].str.strip()

    return df

def get_departments():
    df = load_cinema_data()
    return sorted(df.iloc[:, 1].dropna().unique().tolist())

@routes.route("/get_fauteuils")
def get_fauteuils():
    cinema_name = request.args.get("cinemaName")
    df = load_cinema_data()

    result = df[df['nom'] == cinema_name]['fauteuils']
    if not result.empty:
        fauteuils = int(result.values[0])
    else:
        fauteuils = 0  

    return jsonify(fauteuils=fauteuils)

@routes.route("/get_entrees")
def get_entrees():
    cinema_name = request.args.get("cinemaName")
    df = load_cinema_data()

    result = df[df['nom'] == cinema_name]['entrÃes 2020']
    if not result.empty:
        entrees_2020 = int(result.values[0])
        min_entrees = max(entrees_2020 - 20000, 0)  
        max_entrees = entrees_2020 + 20000
    else:
        min_entrees = 0
        max_entrees = 0

    return jsonify(min_entrees=min_entrees, max_entrees=max_entrees)

@routes.route("/get_cinemas")
def get_cinemas():
    department = request.args.get("department")
    df = load_cinema_data()

    cinemas = df[df.iloc[:, 1] == department]['nom'].dropna().unique().tolist()

    return jsonify(cinemas=sorted(cinemas))

@routes.route("/simulation")
def simulation():
    departments = get_departments()
    return render_template("simulation.html", departments=departments)

@routes.route("/simulate", methods=['POST'])
def simulate():
    try:
        cinema_name = request.form["cinemaName"]
        department = request.form["department"]
        min_entrees = int(request.form["minEntrees"])
        max_entrees = int(request.form["maxEntrees"])
        fauteuils = int(request.form["fauteuils"])
        restrictions = float(request.form["restrictions"])


        plot_html = generate_interactive_plot("models/random_forest_model.pkl" ,min_entrees, max_entrees, fauteuils, restrictions)

        flash(f"Simulation réussie pour {cinema_name}.")

        return render_template("simulation.html", departments=get_departments(), plot_html=plot_html)
    except Exception as e:
        flash(f"Erreur lors de la simulation : {str(e)}", "danger")
        return redirect(url_for('routes.simulation'))

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/dashboard")
def graphs():
    try:
        graphs = [
            {"title": "Répartition des cinémas par département",
             "image": "repartition_cinemas_par_departement.png",
             "details": "Paris (75) domine avec le plus grand nombre de cinémas."},
            {"title": "Répartition des entrées totales par département",
             "image": "repartition_entrees_par_departement.png",
             "details": "Les entrées sont majoritairement concentrées à Paris (75)."},
            {"title": "Comparaison des entrées 2019 vs 2020",
             "image": "comparaison_entrees_2019_2020.png",
             "details": "La pandémie a entraîné une chute des entrées en 2020."},
            {"title": "Performances des cinémas (fauteuils vs entrées 2020)",
             "image": "performances_fauteuils_vs_entrees_2020.png",
             "details": "Les grands cinémas ont tendance à attirer plus de spectateurs."},
            {"title": "Répartition des cinémas par tranche d'entrées annuelles",
             "image": "repartition_cinemas_par_tranche_entrees.png",
             "details": "La majorité des cinémas enregistrent entre 5 000 et 20 000 entrées annuelles."}
        ]
        return render_template("dashboard.html", graphs=graphs)
    except Exception as e:
        flash(f"Erreur lors de la génération des graphiques : {str(e)}", "danger")
        return "Erreur lors de la génération des graphiques"

if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(debug=True)