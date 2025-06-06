import pandas as pd
import re
import spacy
from time import time
import nltk
from nltk.data import find
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys
print(sys.executable)

import nltk
nltk.download('punkt')
nltk.download('word2vec_sample')

import pandas as pd
# Charge le fichier nécessaire (adapte le chemin si besoin)
df = pd.read_csv("/home/miya/Downloads/simpsons_script_lines.csv",low_memory=False)

# Garde uniquement les colonnes utiles
df = df[["raw_character_text", "spoken_words"]]

# Supprime les lignes vides
df.dropna(inplace=True)

# Affiche un aperçu
a = df.head()

print(a)

import spacy


# Utilise le modèle léger de spaCy sans le parser ni la reconnaissance d'entités
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])


def cleaning(doc):
    # Lemmatisation + suppression des stopwords
    txt = [token.lemma_ for token in doc if not token.is_stop]
    return ' '.join(txt) if len(txt) > 2 else None

import re

brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df["spoken_words"])
brief_cleaning = list(brief_cleaning)  # Important !

print(len(brief_cleaning))
print(brief_cleaning[:5])


from time import time

t = time()

# Traitement par lot avec n_process=1 (équivalent à l’ancien n_threads)
txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_process=1)]

print("✅ Nettoyage terminé en", round((time() - t) / 60, 2), "minutes")

df_clean = pd.DataFrame({'clean': txt})
df_clean = df_clean.dropna().drop_duplicates()
df_clean.shape


from gensim.models.phrases import Phrases, Phraser

sent = [row.split() for row in df_clean['clean']]  # Tokenisation simple
phrases = Phrases(sent, min_count=5, threshold=10)
bigram = Phraser(phrases)

sentences = bigram[sent]

print(list(sentences)[:5])

from collections import defaultdict

# Dictionnaire pour stocker la fréquence de chaque mot
word_freq = defaultdict(int)

# Remplir le dictionnaire avec les fréquences
for sent in sentences:
    for word in sent:
        word_freq[word] += 1

# Affichage du nombre de mots uniques
print("Nombre total de mots uniques :", len(word_freq))

# Affichage des 10 mots les plus fréquents
b = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
print(b)

import multiprocessing

from gensim.models import Word2Vec

cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# Entraîner le modèle Word2Vec
w2v_model = Word2Vec(
    sentences=sentences,      # Les phrases tokenisées avec bigrammes
    vector_size=100,          # Taille des vecteurs de mots
    window=5,                 # Fenêtre de contexte
    min_count=5,              # Fréquence minimale pour considérer un mot
    workers=cores - 1         # Nombre de threads parallèles
)

print("✅ Entraînement terminé.")

from time import time

t = time()

# Construction du vocabulaire à partir des phrases
w2v_model.build_vocab(sentences, progress_per=10000)

print("⏱️ Temps de construction du vocabulaire :", round((time() - t) / 60, 2), "minutes")

t = time()

w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

print("✅ Modèle entraîné en", round((time() - t) / 60, 2), "minutes")

# Rendre le modèle plus léger si on ne compte plus l'entraîner
#w2v_model.init_sims(replace=True)

w2v_model.wv.most_similar(positive=["homer"])

w2v_model.wv.most_similar(positive=["homer_simpson"])

w2v_model.wv.most_similar(positive=["marge"])

w2v_model.wv.most_similar(positive=["bart"])

w2v_model.wv.similarity('maggie', 'baby')

#

w2v_model.wv.doesnt_match(['jimbo', 'milhouse', 'kearney'])

w2v_model.wv.most_similar(positive=["woman", "homer"], negative=["marge"], topn=3)

w2v_model.wv.most_similar(positive=["woman", "bart"], negative=["man"], topn=3)

import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline
 
import seaborn as sns
sns.set_style("darkgrid")

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def tsnescatterplot(model, word, list_names):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """
    arrays = np.empty((0, model.vector_size), dtype='f')
    word_labels = [word]
    color_list  = ['red']

    # adds the vector of the query word
    arrays = np.append(arrays, model.wv.__getitem__([word]), axis=0)
    
    # gets list of most similar words
    close_words = model.wv.most_similar([word])
    
    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        wrd_vector = model.wv.__getitem__([wrd_score[0]])
        word_labels.append(wrd_score[0])
        color_list.append('blue')
        arrays = np.append(arrays, wrd_vector, axis=0)
    
    # adds the vector for each of the words from list_names to the array
    for wrd in list_names:
        wrd_vector = model.wv.__getitem__([wrd])
        word_labels.append(wrd)
        color_list.append('green')
        arrays = np.append(arrays, wrd_vector, axis=0)
        
    # Reduces the dimensionality from 300 to 50 dimensions with PCA
    reduc = PCA(n_components=min(len(arrays), model.vector_size)).fit_transform(arrays)
    
    # Finds t-SNE coordinates for 2 dimensions
    np.set_printoptions(suppress=True)
    
    Y = TSNE(n_components=2, random_state=0, perplexity=15).fit_transform(reduc)
    
    # Sets everything up to plot
    df = pd.DataFrame({'x': [x for x in Y[:, 0]],
                       'y': [y for y in Y[:, 1]],
                       'words': word_labels,
                       'color': color_list})
    
    fig, _ = plt.subplots()
    fig.set_size_inches(9, 9)
    
    # Basic plot
    p1 = sns.regplot(data=df,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={'s': 40,
                                  'facecolors': df['color']
                                 }
                    )
    
    # Adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
         p1.text(df["x"][line],
                 df['y'][line],
                 '  ' + df["words"][line].title(),
                 horizontalalignment='left',
                 verticalalignment='bottom', size='medium',
                 color=df['color'][line],
                 weight='normal'
                ).set_size(15)

    
    plt.xlim(Y[:, 0].min()-50, Y[:, 0].max()+50)
    plt.ylim(Y[:, 1].min()-50, Y[:, 1].max()+50)
            
    plt.title('t-SNE visualization for {}'.format(word.title()))

    def tsnescatterplot(model, word, list_names):
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.manifold import TSNE
        import seaborn as sns

        # Initialiser un tableau vide avec la bonne dimension
        arrays = np.empty((0, model.vector_size))
        word_labels = []
        color_list = []

        # Ajouter le vecteur du mot principal
        arrays = np.vstack([arrays, model.wv[word]])
        word_labels.append(word)
        color_list.append('red')

        # Ajouter les mots proches
        close_words = model.wv.most_similar([word])
        for wrd, _ in close_words:
            word_labels.append(wrd)
            color_list.append('orange')
            arrays = np.vstack([arrays, model.wv[wrd]])

        # Ajouter les mots supplémentaires spécifiés
        for wrd in list_names:
            if wrd in model.wv:
                word_labels.append(wrd)
                color_list.append('green')
                arrays = np.vstack([arrays, model.wv[wrd]])

        # Réduction de dimension avec t-SNE
        tsne = TSNE(n_components=2, random_state=0, perplexity=3)
        Y = tsne.fit_transform(arrays)

        # Mise en DataFrame pour affichage
        df = pd.DataFrame({
            "x": Y[:, 0],
            "y": Y[:, 1],
            "words": word_labels,
            "color": color_list
        })

        plt.figure(figsize=(14, 10))
        sns.scatterplot(data=df, x="x", y="y", hue="color", legend=False, s=100)

        # Annoter chaque point
        for i in range(df.shape[0]):
            plt.text(df["x"][i] + 1, df["y"][i] + 1, df["words"][i], fontsize=12)

        plt.title(f"t-SNE visualization for: '{word}'")
        plt.show()

# ✅ Call the function outside
tsnescatterplot(w2v_model, 'homer', ['dog', 'bird', 'ah', 'maude', 'bob', 'mel', 'apu', 'duff'])
