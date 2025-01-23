import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = '/home/40008003/Téléchargements/prix-des-carburants-corrige.csv'
dataset_corrected = pd.read_csv(file_path)

# Preprocessing: focus on relevant columns
relevant_columns = [
    "Prix Gazole", "Prix SP95", "Prix SP98", "Prix E10", "Prix E85", "Prix GPLc", 
    "Région", "code_region", "Département"
]
fuel_data = dataset_corrected[relevant_columns]

# Convert price columns to numeric, handling errors
price_columns = ["Prix Gazole", "Prix SP95", "Prix SP98", "Prix E10", "Prix E85", "Prix GPLc"]
fuel_data[price_columns] = fuel_data[price_columns].apply(pd.to_numeric, errors='coerce')

# Group by region to calculate mean prices
regional_prices = fuel_data.groupby("Région")[price_columns].mean()

# Reset index for visualization
regional_prices.reset_index(inplace=True)

# Generate a bar chart for average fuel prices by region
plt.figure(figsize=(15, 8))
regional_prices.set_index("Région").plot(kind="bar", figsize=(15, 8), stacked=False, alpha=0.75)
plt.title("Moyenne des prix des carburants par région", fontsize=16)
plt.ylabel("Prix moyen (€)", fontsize=12)
plt.xlabel("Région", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.legend(title="Type de carburant")
plt.tight_layout()
plt.show()

# Analyze missing values per region
missing_values = fuel_data.isnull().groupby(fuel_data["Région"]).sum()[price_columns]

# Generate a heatmap for missing data
plt.figure(figsize=(15, 8))
plt.imshow(missing_values, aspect='auto', cmap='viridis')
plt.colorbar(label='Données manquantes (nombre)')
plt.title("Quantité de données manquantes par région et type de carburant", fontsize=16)
plt.xlabel("Type de carburant", fontsize=12)
plt.ylabel("Région", fontsize=12)
plt.xticks(ticks=range(len(price_columns)), labels=price_columns, rotation=45, ha="right", fontsize=10)
plt.yticks(ticks=range(len(missing_values.index)), labels=missing_values.index, fontsize=10)
plt.tight_layout()
plt.show()

# Correlation matrix for price columns
price_corr = fuel_data[price_columns].corr()

# Generate a heatmap for correlation between fuel prices
plt.figure(figsize=(10, 6))
plt.imshow(price_corr, cmap='coolwarm', interpolation='nearest', aspect='auto')
plt.colorbar(label='Corrélation')
plt.title("Corrélation entre les prix des carburants", fontsize=16)
plt.xticks(ticks=range(len(price_columns)), labels=price_columns, rotation=45, ha="right", fontsize=10)
plt.yticks(ticks=range(len(price_columns)), labels=price_columns, fontsize=10)
plt.tight_layout()
plt.show()

# Suggested application name
print("\nSuggestion de nom pour l'application : 'Carburants Malins'")