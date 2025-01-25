import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier `.env`
load_dotenv()

# Récupérer le chemin du fichier CSV depuis les variables d'environnement
file_path = os.getenv("CINEMA_CSV_PATH")

if not file_path:
    raise EnvironmentError("La variable d'environnement 'CINEMA_CSV_PATH' n'est pas définie.")


# Charger le fichier CSV
cinema_data = pd.read_csv(file_path, sep=";")

# Dossier pour enregistrer les images
output_dir = "../app/static/images"
os.makedirs(output_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas

# 1. Répartition des cinémas par département
plt.figure(figsize=(8, 5))
cinema_data["Département"].value_counts().sort_index().plot(kind="bar")
plt.title("Répartition des cinémas par département")
plt.xlabel("Département")
plt.ylabel("Nombre de cinémas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "repartition_cinemas_par_departement.png"))
plt.close()

# 2. Capacité moyenne en sièges selon le statut Multiplexe
cinema_data["Multiplexe"] = cinema_data["Multiplexe"].str.upper()  # Uniformiser "OUI" et "NON"
multiplexe_mean_seats = cinema_data.groupby("Multiplexe")["fauteuils"].mean()

plt.figure(figsize=(6, 4))
multiplexe_mean_seats.plot(kind="bar", color=["blue", "orange"], width=0.6)
plt.title("Capacité moyenne en sièges par type de cinéma")
plt.xlabel("Multiplexe")
plt.ylabel("Nombre moyen de sièges")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "capacite_moyenne_sieges_par_multiplexe.png"))
plt.close()

# 3. Distribution de la part de marché des films français (Art et Essai vs autres)
cinema_data["catégorie Art et Essai"] = cinema_data["catégorie Art et Essai"].str.upper()  # Uniformiser
art_et_essai_data = cinema_data[["catégorie Art et Essai", "PdM en entrées des films français 2020"]]

plt.figure(figsize=(8, 5))
art_et_essai_data.boxplot(by="catégorie Art et Essai", column="PdM en entrées des films français 2020", grid=False)
plt.title("Distribution des parts de marché des films français (2020)")
plt.suptitle("")  # Supprimer le titre par défaut
plt.xlabel("Catégorie Art et Essai")
plt.ylabel("Part de marché (%)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "distribution_parts_marche_films_francais.png"))
plt.close()

# 4. Répartition des cinémas par tranche d'entrées annuelles
plt.figure(figsize=(8, 5))
cinema_data["Tranche d'entrées annuelles"].value_counts().sort_values(ascending=True).plot(kind="barh", color="purple")
plt.title("Répartition des cinémas par tranche d'entrées annuelles")
plt.xlabel("Nombre de cinémas")
plt.ylabel("Tranche d'entrées annuelles")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "repartition_cinemas_par_tranche_entrees.png"))
plt.close()

print(f"Les graphiques ont été enregistrés dans le dossier : {output_dir}")
