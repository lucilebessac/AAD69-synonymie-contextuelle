import torch
import torch.serialization
from numpy.core.multiarray import _reconstruct
import pandas as pd
from spacy_conll import init_parser
import json

# Pour gérer l'erreur Pytorch / STanza
torch.serialization.add_safe_globals([_reconstruct])

# Problème sur la fonction torch.load / weights_only=False
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# Fonction pour analyser le texte avec Stanza via Spacy
def analyse_texte_et_generer_conll(texte):
    # Initialisation du parser
    nlp = init_parser("fr",
                      "stanza",
                      parser_opts={"use_gpu": True, "verbose": False},
                      include_headers=True)

    # Analyser le texte
    doc = nlp(texte)

    # Générer le fichier .conll
    conll = doc._.conll_str
    with open("eau.conll", "w", encoding="utf-8") as f:
        f.write(conll)

    # Convertir en DataFrame
    conll_df = doc._.conll_pd
    conll_df.to_csv("eau.csv", sep="\t", index=False)

    return conll_df

# Fonction pour extraire les relations de dépendance et les propositions
def extraire_relations_et_propositions(conll_df):
    # Liste des mots à ignorer (stop words)
    stop_words = ["le", "la", "les", "à", "de", "en", "et", "sous", "dans"]

    # Dictionnaire pour stocker les résultats
    dico_enonces = {}

    # Liste des arguments principaux dans les relations de dépendance
    liste_core_arguments = ["nsubj", "obj", "iobj", "ccomp", "advmod"]
    propositions = []

    # Traiter chaque ligne du DataFrame (chaque token)
    for idx, row in conll_df.iterrows():
        liste_core_arguments_locale = []
        proposition = []

        if row['form'].lower() not in stop_words:  # Ignorer les mots inutiles
            if row['deprel'] == 'root' and row['upos'] == 'VERB':
                liste_core_arguments_locale.append(row['id'])
                proposition.append(row['form'])

                id_head = row['id']
                for _, token2 in conll_df.iterrows():
                    if token2['head'] == id_head and token2['deprel'] in liste_core_arguments:
                        liste_core_arguments_locale.append(token2['id'])
                        proposition.append(token2['form'])

            elif row['deprel'] == 'root' and row['upos'] == 'ADJ':
                liste_core_arguments_locale.append(row['id'])
                proposition.append(row['form'])

                id_head = row['id']
                for _, token2 in conll_df.iterrows():
                    if token2['head'] == id_head and (token2['deprel'] in liste_core_arguments or token2['deprel'] == 'cop'):
                        liste_core_arguments_locale.append(token2['id'])
                        proposition.append(token2['form'])

            elif row['upos'] == 'VERB':
                liste_core_arguments_locale.append(row['id'])
                proposition.append(row['form'])

                id_head = row['id']
                for _, token2 in conll_df.iterrows():
                    if token2['head'] == id_head and token2['deprel'] in liste_core_arguments:
                        liste_core_arguments_locale.append(token2['id'])
                        proposition.append(token2['form'])

        # Sauvegarde les informations pour chaque phrase
        if proposition:
            propositions.append(" ".join(proposition))

    # Création du dictionnaire avec les résultats extraits
    dico_enonces = {
        "propositions": propositions,
        "relations": [liste_core_arguments_locale]
    }

    return dico_enonces

# Texte d'exemple à analyser
phrase = "Le bois est plus léger que l'eau puisqu'il flotte lorsqu'on l'enfonce dans l'eau."

# Analyse du texte et génération du fichier CoNLL
conll_df = analyse_texte_et_generer_conll(phrase)

# Extraction des relations de dépendance et des propositions
resultats = extraire_relations_et_propositions(conll_df)

# Sauvegarde les résultats dans un fichier JSON
with open("propositions_extraites.json", "w", encoding="utf-8") as outfile:
    json.dump(resultats, outfile, ensure_ascii=False, indent=4)

# Affichage des résultats
print("Propositions extraites :")
for prop in resultats['propositions']:
    print(prop)
