from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
from app.model import generate_interactive_plot  # Assurez-vous que le chemin est correct

# Blueprint et app Flask
routes = Blueprint("routes", __name__, template_folder="templates")

app = Flask(__name__, template_folder="app/templates")
app.secret_key = "secret_key"  # Clé secrète pour les messages flash

# Fonction pour charger les données du fichier CSV
def load_cinema_data():
    file_path = "data/raw/les_salles_de_cinemas_en_ile-de-france.csv"
    df = pd.read_csv(file_path, sep=";", encoding="ISO-8859-1")

    # Nettoyage des données
    df.columns = df.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)
    df.iloc[:, 1] = df.iloc[:, 1].astype(str).str.strip()  # 2ème colonne pour les départements
    df['nom'] = df['nom'].str.strip()

    return df

# Obtenir la liste des départements uniques (2e colonne)
def get_departments():
    df = load_cinema_data()
    return sorted(df.iloc[:, 1].dropna().unique().tolist())

# API pour obtenir les cinémas d'un département donné (en utilisant la 2e colonne pour le filtre)
@routes.route("/get_cinemas")
def get_cinemas():
    department = request.args.get("department")
    df = load_cinema_data()

    # Filtrer les cinémas du département sélectionné
    cinemas = df[df.iloc[:, 1] == department]['nom'].dropna().unique().tolist()

    # Debug : Afficher les cinémas trouvés
    print(f"Cinémas trouvés pour {department} :", cinemas)

    return jsonify(cinemas=sorted(cinemas))

# Page de simulation
@routes.route("/simulation")
def simulation():
    departments = get_departments()
    return render_template("simulation.html", departments=departments)

# Traiter la simulation
@routes.route("/simulate", methods=['POST'])
def simulate():
    try:
        # Récupérer les données du formulaire
        cinema_name = request.form["cinemaName"]
        department = request.form["department"]
        min_entrees = int(request.form["minEntrees"])
        max_entrees = int(request.form["maxEntrees"])
        fauteuils = int(request.form["fauteuils"])
        restrictions = float(request.form["restrictions"])

        # Calcul de l'impact simple
        impact = (min_entrees + max_entrees) / 2 * restrictions / 100

        # Appel à la fonction generate_interactive_plot pour générer une prédiction
        plot_html = generate_interactive_plot(min_entrees, max_entrees, fauteuils, restrictions)

        flash(f"Simulation réussie pour {cinema_name}. Impact estimé : {impact:.2f}")
        return render_template("simulation.html", departments=get_departments(), plot_html=plot_html)
    except Exception as e:
        flash(f"Erreur lors de la simulation : {str(e)}", "danger")
        return redirect(url_for('routes.simulation'))

# Route pour la page d'accueil
@routes.route("/")
def index():
    return render_template("index.html")

# Route pour afficher les graphiques
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