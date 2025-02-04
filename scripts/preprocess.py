import pandas as pd
import os as os

def preprocess_data(input_file, output_file):
    data = pd.read_csv(input_file, sep=';')

    # Remplissage des données manquantes
    data['entrées 2019'] = data['entrées 2019'].fillna(data['entrées 2019'].mean())
    data['entrées 2020'] = data['entrées 2020'].fillna(data['entrées 2020'].mean())
    data['fauteuils'] = data['fauteuils'].fillna(data['fauteuils'].median())

    # Encodage des variables catégoriques
    # data['Multiplexe'] = data['Multiplexe'].apply(lambda x: 1 if x == "OUI" else 0)

    # 1. Calcul de la durée de fermeture en fonction de la baisse des entrées entre 2019 et 2020
    data['duree_fermeture'] = (1 - (data['entrées 2020'] / data['entrées 2019'])).clip(0, 1) * 6  # Fermeture maximale de 6 mois (car COVID)

    # 2. Simulation des restrictions en fonction de la baisse des entrées
    data['restrictions'] = (1 - (data['entrées 2020'] / data['entrées 2019'])).clip(0, 1) * 100  # Restrictions entre 0 % et 100 %

    # 3. Taux de reprise après réouverture
    data['taux_reprise'] = (data['entrées 2020'] / data['entrées 2019']).clip(0, 1)

    # Sauvegarde des données nettoyées
    data.to_csv(output_file, index=False)
    print("Données prétraitées et sauvegardées.\n\n")

    print("Data cleaned : \n",data)

if __name__ == "__main__":
    # file = os.getenv('CINEMA_CSV_PATH')
    # print ("file : ",file)
    preprocess_data("../data/raw/les_salles_de_cinemas_en_ile-de-france.csv", "../data/processed/cinemas_cleaned.csv") # TODO add env variable for output file 
