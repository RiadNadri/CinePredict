import pandas as pd
import os as os

def preprocess_data(input_file, output_file):
    data = pd.read_csv(input_file, sep=';')

    # Remplissage des données manquantes
    data['entrées 2019'] = data['entrées 2019'].fillna(data['entrées 2019'].mean())
    data['entrées 2020'] = data['entrées 2020'].fillna(data['entrées 2020'].mean())
    data['fauteuils'] = data['fauteuils'].fillna(data['fauteuils'].median())


    data['restrictions'] = (1 - (data['entrées 2020'] / data['entrées 2019'])).clip(0, 1) * 100  # Restrictions entre 0 % et 100 %

    data['taux_reprise_historique'] = (data['entrées 2020'] / data['entrées 2019']).clip(0, 1)

    data.to_csv(output_file, index=False)
    print("Données prétraitées et sauvegardées.\n\n")

    print("Data cleaned : \n",data)

if __name__ == "__main__":

    preprocess_data("../data/raw/les_salles_de_cinemas_en_ile-de-france.csv", "../data/processed/cinemas_cleaned.csv") # TODO add env variable for output file 
