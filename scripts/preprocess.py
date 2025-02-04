import pandas as pd
import os as os

def preprocess_data(input_file, output_file):
    data = pd.read_csv(input_file, sep=';')

    # Remplissage des données manquantes
    data['entrées 2019'] = data['entrées 2019'].fillna(data['entrées 2019'].mean())
    data['fauteuils'] = data['fauteuils'].fillna(data['fauteuils'].median())

    # Encodage des variables catégoriques
    data['Multiplexe'] = data['Multiplexe'].apply(lambda x: 1 if x == "OUI" else 0)

    # Sauvegarde des données nettoyées
    data.to_csv(output_file, index=False)
    print("Données prétraitées et sauvegardées.\n\n")

    print("Data cleaned : \n",data)

if __name__ == "__main__":
    # file = os.getenv('CINEMA_CSV_PATH')
    # print ("file : ",file)
    preprocess_data("../data/raw/les_salles_de_cinemas_en_ile-de-france.csv", "../data/processed/cinemas_cleaned.csv") # TODO add env variable for output file 
