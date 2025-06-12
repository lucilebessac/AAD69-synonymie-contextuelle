# Étude historique et comparative de différentes méthodes de sémantique distributionnelle sur la base d’un corpus ParlaMint

Ce projet propose **trois méthodes distinctes** de sémantique distributionnelle sur la base d’un corpus ParlaMint

1. **🧠 Approche Word2Vec** : Analyse distributionnelle classique avec clustering
2. **🔍 Approche Syntaxique (GrewPy)** : Extraction d'énoncés élémentaires par motifs syntaxiques
3. **🧮 Approche de Cooccurrence** : Matrice de Cooccurrence (DSM) en R Studio

---

## 🧠 Analyse sémantique avec Word2Vec

Cette approche utilise les **représentations vectorielles distribuées** pour identifier des regroupements sémantiques dans le vocabulaire parlementaire.

### 📌 Objectifs
* Apprendre des représentations vectorielles distribuées pour les mots du corpus
* Réduire la dimension pour faciliter l'exploration visuelle
* Identifier des regroupements sémantiques via clustering hiérarchique
* Extraire des mots représentatifs et spécifiques pour chaque cluster (représentants et parangons)

### 🔁 Pipeline des scripts (ordre d'exécution)
1. **Prétraitement du corpus** → `02_preprocess.py`  
   Nettoyage du texte, lemmatisation, suppression des stopwords
2. **Construction des bigrammes** → `03_bigramm.py`  
   Identification des expressions fréquentes pour enrichir le contexte
3. **Entraînement du modèle Word2Vec** → `04_train_word2vec.py`  
   Modèle entraîné en Skip-gram avec Gensim
4. **Réduction de dimension (PCA)** → `05_reduce_dimensions.py`  
   Réduction à 20 dimensions (pour clustering), puis 2D (visualisation)
5. **Clusterisation hiérarchique (Ward, k=10)** → `Ward_clustering.py`  
   Attribution d'un cluster à chaque mot selon la méthode de Ward
6. **Visualisation des clusters (k=10)** → `07_Ward_visualization.py`  
   Projection 2D par PCA, mots colorés selon leur cluster
7. **Dendrogramme hiérarchique** → `08_dindogramme.py`  
   Représentation arborescente des fusions de clusters
8. **Méthode du coude (inertie intra-classe)** → `09_marches_d'inertie.py`  
   Aide à identifier un nombre optimal de clusters
9. **Clusterisation alternative (k=3)** → `10_Ward_clustering_k=3.py`  
   Réduction de granularité pour plus de lisibilité thématique
10. **Visualisation (Ward, k=3)** → `11_Ward_visualisation_k=3.py`
11. **Extraction des représentants et parangons** → `12_représenatants_parangons.py`  
    Calcul des mots typiques et spécifiques à chaque cluster

### 📂 Données produites
* `word2vec.model` — modèle Word2Vec entraîné
* `X_reduced.npy` — vecteurs Word2Vec réduits (20D)
* `words.pkl` — liste des mots alignés avec `X_reduced`
* `mots_clusters_ward.csv` — affectation des mots aux clusters
* `representants_parangons_k3.csv` — mots typiques et discriminants par cluster

### 📊 Visualisations Word2Vec
* `clusters_ward_pca.png` — Projection 2D des clusters (k=10)
* `dendrogramme_ward.png` — Dendrogramme hiérarchique (Ward)
* `inertie_dendrogramme_coude.png` — Méthode du coude (inertie vs. k)
* `clusters_k3.png` — Clusters réduits à k=3
* `représentants.png` — Mots proches du centroïde (représentants)
* `parangons.png` — Mots les plus spécifiques par cluster

---

## Approche Syntaxique avec GrewPy

Cette approche se concentre sur l'**extraction d'énoncés élémentaires** basée sur des motifs syntaxiques spécifiques.

### 📌 Objectifs
* Extraire automatiquement les énoncés élémentaires du corpus ParlaMint 2018
* Identifier les structures syntaxiques récurrentes (Déterminant-Nom-Auxiliaire-Verbe)
* Générer des fichiers CoNLL pour l'analyse syntaxique
* Indexer et filtrer les énoncés selon des critères linguistiques

### Pipeline syntaxique
1. **Génération CoNLL** → `generate_conll()`  
   Conversion du corpus textuel en format CoNLL via Stanza
2. **Chargement du corpus** → `grewpy.Corpus()`  
   Chargement des fichiers CoNLL pour l'analyse syntaxique
3. **Recherche de motifs** → Pattern matching avec GrewPy  
   ```
   pattern {
       X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;
       Y-[det]->Z;
       X-[aux:pass|aux:tense]->W;
   }
   ```
4. **Indexation** → `indexe_enonces_elem()`  
   Extraction des formes lemmatisées (D1, N1, AUX, V)
5. **Export** → Génération du fichier `enonces_elementaires.txt`

### Données produites (GrewPy)
* `*.conll` — Fichiers d'analyse syntaxique (format CoNLL-U)
* `enonces_elementaires.txt` — Énoncés extraits sous forme textuelle
* Structure indexée des énoncés avec métadonnées linguistiques

### Scripts utilitaires
* **Renumérotation des sent_id** — Script pour harmoniser l'indexation des phrases dans les fichiers CoNLL

---

## 🧮 Approche de Cooccurrence** : Matrice de Cooccurrence (DSM) en R Studio

Cette méthode s’appuie sur une matrice de cooccurrences pondérée par PPMI.

### 📌 Objectifs
* Nettoyer et tokeniser les fichiers du corpus ParlaMint
* Construire une matrice creuse de cooccurrence (DSM)
* Appliquer le score PPMI (Positive Pointwise Mutual Information)
* Réduire la dimension via MDS ou PCA
* Identifier des groupes sémantiques par k-means
* Visualiser l’espace sémantique en 2D

### 🔁 Pipeline des scripts (ordre d’exécution)
1. **Lecture des fichiers du corpus**
   Chargement de fichiers .txt, suppression des lignes vides et du bruit typographique
2. **Tokenisation + nettoyage**
   Mise en minuscules, suppression de ponctuation, mots courts, stopwords
3. **Extraction des cooccurrences** (fenêtre glissante)
   Création de triplets (mot, contexte, poids)
4. **Construction de la matrice DSM**
   Matrice terme x contexte au format creux (Matrix::sparseMatrix)
5. **Pondération avec PPMI**
   Transformation des cooccurrences brutes en scores informatifs
6. **Réduction de dimension (MDS ou PCA)**
   Projection 2D pour visualisation
7. **Clusterisation par k-means**
   Identification de groupes lexicaux
8. **Visualisation finale**
   Représentation graphique avec factoextra::fviz_cluster()

📂 Données produites
* dsm_ppmi — Matrice DSM (terme x contexte) pondérée par PPMI
* coords_kmeans — Coordonnées MDS des mots pour affichage
* mat_top — Matrice dense réduite aux mots les plus fréquents
* clustering$cluster — Affectation des mots aux clusters
* Graphiques générés : clustering par MDS et PCA

## Installation et Dépendances

### Dépendances communes
```bash
pip install -r requirements.txt
```

### Approche Word2Vec
* `gensim`
* `numpy` (recommandé : version 1.24.x pour compatibilité Gensim)
* `pandas`
* `scikit-learn`
* `matplotlib`
* `seaborn`

### Approche GrewPy
* `grewpy` (≥0.4.0)
* `spacy-conll` (≥1.4.0)
* `stanza` (≥1.4.0)
* `torch` (≥1.9.0)
* `numpy` (≥1.21.0)

### Approche de Cooccurrence
* installer ces bibliothèques sur R
  ```
  install.packages(c(
  "wordspace", 
  "stopwords", 
  "Matrix", 
  "factoextra"))
```
