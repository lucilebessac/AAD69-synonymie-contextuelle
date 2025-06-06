import pandas as pd
import numpy as np
import re
from gensim.models import Word2Vec
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. Chargement et nettoyage du corpus
# ------------------------------------
df = pd.read_csv(
    "/home/miya/Downloads/simpsons_script_lines.csv",
    dtype={'raw_text': str},
    low_memory=False
)
df['raw_text'] = df['raw_text'].astype(str).str.lower()

# Nettoyage basique : suppression de la ponctuation
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text

df['raw_text_clean'] = df['raw_text'].apply(clean_text)

# 2. Tokenisation des phrases
# ---------------------------
sentences = df['raw_text_clean'].apply(lambda x: x.split()).tolist()

# 3. Entraînement du modèle Word2Vec
# ----------------------------------
w2v_model = Word2Vec(
    sentences,
    vector_size=100,  # Taille des vecteurs, ajustable
    window=5,
    min_count=2,
    workers=4,
    sg=1  # Skip-gram
)

# 4. Calcul des vecteurs de phrases (moyenne des vecteurs de mots)
# ---------------------------------------------------------------
def get_sentence_vector(sentence, model):
    vectors = [model.wv[w] for w in sentence if w in model.wv]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

sentence_vectors = np.array([get_sentence_vector(sent, w2v_model) for sent in sentences])
print("Shape des vecteurs de phrases :", sentence_vectors.shape)

# 5. Sous-échantillonnage si trop de phrases pour le clustering hiérarchique
# --------------------------------------------------------------------------
MAX_CLUSTER_SIZE = 5000  # Limite raisonnable pour AgglomerativeClustering
if len(sentence_vectors) > MAX_CLUSTER_SIZE:
    print(f"Le corpus est trop volumineux ({len(sentence_vectors)} phrases) pour un clustering hiérarchique.")
    print(f"Un sous-échantillon aléatoire de {MAX_CLUSTER_SIZE} phrases sera utilisé pour le clustering et la visualisation.")
    idx = np.random.choice(len(sentence_vectors), MAX_CLUSTER_SIZE, replace=False)
    sentence_vectors_sample = sentence_vectors[idx]
    df_sample = df.iloc[idx].reset_index(drop=True)
else:
    sentence_vectors_sample = sentence_vectors
    df_sample = df.reset_index(drop=True)

# 6. Clusterisation hiérarchique avec choix automatique du nombre de clusters
# --------------------------------------------------------------------------
range_n_clusters = range(2, 11)
best_score = -1
best_k = 2
for n_clusters in range_n_clusters:
    clusterer = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    cluster_labels = clusterer.fit_predict(sentence_vectors_sample)
    score = silhouette_score(sentence_vectors_sample, cluster_labels)
    print(f"Silhouette pour {n_clusters} clusters : {score:.3f}")
    if score > best_score:
        best_score = score
        best_k = n_clusters

print(f"Nombre optimal de clusters : {best_k}")

# Clusterisation finale avec le nombre optimal de clusters
final_clusterer = AgglomerativeClustering(n_clusters=best_k, linkage='ward')
final_labels = final_clusterer.fit_predict(sentence_vectors_sample)
df_sample['cluster'] = final_labels

# 7. Visualisation des clusters en 2D avec PCA
# --------------------------------------------
pca = PCA(n_components=2)
reduced = pca.fit_transform(sentence_vectors_sample)

plt.figure(figsize=(8,6))
scatter = plt.scatter(reduced[:,0], reduced[:,1], c=final_labels, cmap='tab10', alpha=0.7)
plt.title("Clusters hiérarchiques des phrases (PCA)")
plt.xlabel("Composante principale 1")
plt.ylabel("Composante principale 2")
plt.colorbar(scatter, label='Cluster')
plt.show()

# 8. Exploration : Afficher quelques phrases par cluster
# -----------------------------------------------------
for cluster_id in range(best_k):
    print(f"\n=== Exemples du cluster {cluster_id} ===")
    exemples = df_sample[df_sample['cluster'] == cluster_id]['raw_text'].head(3)
    for phrase in exemples:
        print("-", phrase)
