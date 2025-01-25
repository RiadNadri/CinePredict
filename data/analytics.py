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

# Répartition des entrées totales par département
dept_entrees = cinema_data.groupby("Département")["entrées 2020"].sum().sort_values()

plt.figure(figsize=(10, 6))
dept_entrees.plot(kind="bar", color="skyblue")
plt.title("Répartition des entrées totales par département (2020)")
plt.xlabel("Département")
plt.ylabel("Nombre total d'entrées")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "repartition_entrees_par_departement.png"))
plt.close()


# Comparaison des entrées 2019 et 2020
plt.figure(figsize=(8, 6))
plt.scatter(cinema_data["entrées 2019"], cinema_data["entrées 2020"], alpha=0.7)
plt.title("Comparaison des entrées 2019 vs 2020")
plt.xlabel("Entrées 2019")
plt.ylabel("Entrées 2020")
plt.axline((0, 0), slope=1, color="red", linestyle="--", label="Ligne y=x")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "comparaison_entrees_2019_2020.png"))
plt.close()

# Scatter plot des performances selon les fauteuils et entrées 2020
plt.figure(figsize=(8, 6))
plt.scatter(cinema_data["fauteuils"], cinema_data["entrées 2020"], alpha=0.7, color="blue")
plt.title("Performances des cinémas : Fauteuils vs Entrées 2020")
plt.xlabel("Nombre de fauteuils")
plt.ylabel("Entrées 2020")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "performances_fauteuils_vs_entrees_2020.png"))
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
