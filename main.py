import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from tensorflow.image import resize

# ---------------------------
# Étape 1 : Charger le dataset
# ---------------------------
def load_and_normalize_data():
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    return x_train, y_train, x_test, y_test

# ---------------------------
# Étape 2 : Associer une météo à chaque catégorie
# ---------------------------
def assign_weather(category):
    weather_map = {
        0: 'Chaud',        # T-shirt
        1: 'Mi-saison',    # Pantalon
        2: 'Froid',        # Pull
        3: 'Chaud',        # Robe
        4: 'Froid',        # Manteau
        5: 'Chaud',        # Sandales
        6: 'Mi-saison',    # Chemise
        7: 'Pluie',        # Baskets
        8: 'Indépendant',  # Sac
        9: 'Froid'         # Bottes
    }
    return weather_map[category]


def classify_clothing(category):
    type_map = {
        0: 'haut',        # T-shirt
        1: 'bas',         # Pantalon
        2: 'haut',        # Pull
        3: 'haut',        # Robe
        4: 'haut',        # Manteau
        5: 'chaussures',  # Sandales
        6: 'haut',        # Chemise
        7: 'chaussures',  # Baskets
        8: 'autre',       # Sac
        9: 'chaussures',  # Bottes
        # Ajoute d'autres catégories si nécessaire
    }
    return type_map.get(category, 'autre')


# ---------------------------
# Étape 3 : Prétraiter les images pour ResNet50
# ---------------------------
def preprocess_images(images):
    # Ajouter un canal pour passer de (28, 28) à (28, 28, 1)
    images_with_channels = np.expand_dims(images, axis=-1)
    # Redimensionner à (224, 224) et simuler RGB en dupliquant les canaux
    resized_images = np.array([resize(img, (224, 224)).numpy() for img in images_with_channels])
    resized_images = np.repeat(resized_images, 3, axis=-1)  # Dupliquer pour avoir 3 canaux
    return preprocess_input(resized_images)


# ---------------------------
# Étape 4 : Extraire les caractéristiques avec ResNet50
# ---------------------------
def extract_features(images):
    resnet = ResNet50(weights='imagenet', include_top=False, pooling='avg')
    return resnet.predict(images)

# ---------------------------
# Étape 5 : Clustering avec k-means
# ---------------------------
def perform_kmeans(features, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features)
    return clusters

def preview_clusters(clusters, x_train, n_samples=5):
    unique_clusters = np.unique(clusters)
    for cluster_id in unique_clusters:
        print(f"Cluster {cluster_id}:")
        indices = np.where(clusters == cluster_id)[0]
        sample_images = x_train[indices][:n_samples]
        plt.figure(figsize=(10, 5))
        for i, img in enumerate(sample_images):
            plt.subplot(1, n_samples, i + 1)
            plt.imshow(img, cmap='gray')
            plt.axis('off')
        plt.suptitle(f"Échantillons du Cluster {cluster_id}")
        plt.show()

# ---------------------------
# Étape 6 : Visualisation avec t-SNE
# ---------------------------
def visualize_clusters(features, clusters):
    tsne = TSNE(n_components=2, random_state=42)
    data_2d = tsne.fit_transform(features)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=clusters, cmap='viridis')
    plt.colorbar()
    plt.title("Clusters de vêtements basés sur la météo")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.show()

# ---------------------------
# Étape 7 : Recommander des vêtements pour une météo
# ---------------------------
def recommend_for_weather(cluster_id, clusters, x_train, cluster_weather_map):
    indices = np.where(clusters == cluster_id)[0]
    recommended_images = x_train[indices]
    
    plt.figure(figsize=(10, 5))
    for i in range(min(10, len(recommended_images))):
        plt.subplot(2, 5, i + 1)
        plt.imshow(recommended_images[i], cmap='gray')
        plt.axis('off')
    plt.suptitle(f"Vêtements recommandés pour {cluster_weather_map[cluster_id]}")
    plt.show()

# ---------------------------
# Main : Exécuter toutes les étapes
# ---------------------------
if __name__ == "__main__":
    # Charger et normaliser les données
    x_train, y_train, _, _ = load_and_normalize_data()
    
    # Associer les étiquettes météo
    weather_labels_train = np.array([assign_weather(label) for label in y_train])
    
    # Prétraiter un sous-ensemble des images pour ResNet50
    x_train_resized = preprocess_images(x_train[:1000])  # Limiter à 1000 pour aller plus vite
    
    # Extraire les caractéristiques
    x_train_features = extract_features(x_train_resized)
    
    # Appliquer k-means
    clusters = perform_kmeans(x_train_features, n_clusters=4)

    preview_clusters(clusters, x_train)
    
    # Visualiser les clusters
    visualize_clusters(x_train_features, clusters)
    
    # Associer les clusters aux conditions météo
    cluster_weather_map = {
        0: 'Chaud',
        1: 'Froid',
        2: 'Mi-saison',
        3: 'Pluie'
    }
    
    # Recommander des vêtements pour une météo
    recommend_for_weather(1, clusters, x_train, cluster_weather_map)  # Exemple : "Froid"
