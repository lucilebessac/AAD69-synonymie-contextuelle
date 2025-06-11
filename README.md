# 🧠 Analyse sémantique avec Word2Vec

Ce dossier contient les scripts nécessaires à la construction, la réduction, la visualisation et l’analyse sémantique d’un modèle Word2Vec entraîné sur un corpus parlementaire.

## 📌 Objectifs

- Apprendre des représentations vectorielles distribuées pour les mots du corpus.
- Réduire la dimension pour faciliter l’exploration visuelle.
- Identifier des regroupements sémantiques via clustering hiérarchique.
- Extraire des mots représentatifs et spécifiques pour chaque cluster (représentants et parangons).

---

## 🔁 Pipeline des scripts (ordre d’exécution)

1. **Prétraitement du corpus**
   → `02_preprocess.py`
   Nettoyage du texte, lemmatisation, suppression des stopwords.

2. **Construction des bigrammes**
   → `03_bigramm.py`
   Identification des expressions fréquentes pour enrichir le contexte.

3. **Entraînement du modèle Word2Vec**
   → `04_train_word2vec.py`
   Modèle entraîné en Skip-gram avec Gensim.

4. **Réduction de dimension (PCA)**
   → `05_reduce_dimensions.py`
   Réduction à 20 dimensions (pour clustering), puis 2D (visualisation).

5. **Clusterisation hiérarchique (Ward, k=10)**
   → `Ward_clustering.py`
   Attribution d’un cluster à chaque mot selon la méthode de Ward.

6. **Visualisation des clusters (k=10)**
   → `07_Ward_visualization.py`
   Projection 2D par PCA, mots colorés selon leur cluster.

7. **Dendrogramme hiérarchique**
   → `08_dindogramme.py`
   Représentation arborescente des fusions de clusters.

8. **Méthode du coude (inertie intra-classe)**
   → `09_marches_d'inertie.py`
   Aide à identifier un nombre optimal de clusters.

9. **Clusterisation alternative (k=3)**
   → `10_Ward_clustering_k=3.py`
   Réduction de granularité pour plus de lisibilité thématique.

10. **Visualisation (Ward, k=3)**
    → `11_Ward_visualisation_k=3.py`

11. **Extraction des représentants et parangons**
    → `12_représenatants_parangons.py`
    Calcul des mots typiques et spécifiques à chaque cluster.

---

## 📂 Données produites

- `word2vec.model` — modèle Word2Vec entraîné
- `X_reduced.npy` — vecteurs Word2Vec réduits (20D)
- `words.pkl` — liste des mots alignés avec `X_reduced`
- `mots_clusters_ward.csv` — affectation des mots aux clusters
- `representants_parangons_k3.csv` — mots typiques et discriminants par cluster

---

## 📊 Visualisations

- `clusters_ward_pca.png` — Projection 2D des clusters (k=10)
- `dendrogramme_ward.png` — Dendrogramme hiérarchique (Ward)
- `inertie_dendrogramme_coude.png` — Méthode du coude (inertie vs. k)
- `clusters_k3.png` — Clusters réduits à k=3
- `représentants.png` — Mots proches du centroïde (représentants)
- `parangons.png` — Mots les plus spécifiques par cluster

---

## 🛠️ Dépendances

- `gensim`
- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `seaborn`

> 💡 *Conseil : installe un environnement virtuel avec `numpy==1.24.x` pour éviter les conflits avec Gensim.*

---

