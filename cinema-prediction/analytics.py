import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
file_path = "C:\Dev\Sources\les_salles_de_cinemas_en_ile-de-france_updated.csv"
cinema_data = pd.read_csv(file_path, sep=";")

# 1. Répartition des cinémas par département
plt.figure(figsize=(8, 5))
cinema_data["Département"].value_counts().sort_index().plot(kind="bar")
plt.title("Répartition des cinémas par département")
plt.xlabel("Département")
plt.ylabel("Nombre de cinémas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

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
plt.show()

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
plt.show()

# 4. Répartition des cinémas par tranche d'entrées annuelles
plt.figure(figsize=(8, 5))
cinema_data["Tranche d'entrées annuelles"].value_counts().sort_values(ascending=True).plot(kind="barh", color="purple")
plt.title("Répartition des cinémas par tranche d'entrées annuelles")
plt.xlabel("Nombre de cinémas")
plt.ylabel("Tranche d'entrées annuelles")
plt.tight_layout()
plt.show()