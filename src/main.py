#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:21:23 

Pour un Corpus (object GrewPy), une request et un parametre donné, donne les mots qu'il ya derrière
Grâce au numéro de node, on peut récupérer le mot correspondant dans le corpus
Grâce au module features

@author: hugodumoulin

Modified on 06/06/2025

@by: Lucile Bessac

"""


import grewpy

def indexe_enonces_elem(corpus, liste_match, param):
    grewpy.set_config("sud")
    print("LISTE DES MATCHS\n")
    for element in liste_match:
        print(element)

    liste_des_enonces_elem = []
    n = 0

    for match in liste_match:
        sent_id = match["sent_id"]
        formes_EE = {}
        nodes = match["matching"]["nodes"]

        formes_EE["D1"] = corpus[sent_id].features[str(nodes["Z"])][param] if "Z" in nodes else ""
        formes_EE["N1"] = corpus[sent_id].features[str(nodes["Y"])][param] if "Y" in nodes else ""
        formes_EE["AUX"] = corpus[sent_id].features[str(nodes["W"])][param] if "W" in nodes else ""
        formes_EE["V"] = corpus[sent_id].features[str(nodes["X"])][param] if "X" in nodes else ""

        dico_un_enonce_elem = {
            "id_EE": n + 1,
            "id_sent": sent_id,
            "formes_EE": formes_EE,
        }
        liste_des_enonces_elem.append(dico_un_enonce_elem)
        n += 1

    return liste_des_enonces_elem


def supprimer_doublons_semantiques(enonces):
    uniques = {}

    for e in enonces:
        cle = (e["id_sent"], e["formes_EE"]["N1"], e["formes_EE"]["V"])
        score = sum(1 for v in e["formes_EE"].values() if v != "")

        if cle not in uniques or score > uniques[cle][0]:
            uniques[cle] = (score, e)

    return [val[1] for val in uniques.values()]

def generate_conll(text, filename):
    """
    Génère un fichier CoNLL à partir d'un texte donné en utilisant Stanza.
    :param text: Texte à analyser
    :param filename: Nom du fichier de sortie (sans extension)
    """
    nlp = init_parser("fr",
                    "stanza",
                    parser_opts={"use_gpu": True, "verbose": False},
                    include_headers=True)
    doc = nlp(text)

    # sauvegarder au format .conll
    conll = doc._.conll_str
    with open(f"{filename}.conll", "w", encoding="utf-8") as f:
        f.write(conll)

    conll_df = doc._.conll_pd
    conll_df.to_csv(f"{filename}.csv", sep="\t", index=False)


if __name__ == "__main__":

    """
    Exemple d'utilisation de la fonction indexe_enonces_elem pour extraire les énoncés élémentaires
    d'un corpus GrewPy à partir de motifs donnés.
    """
    # Génération d'un fichier CoNLL à partir d'un texte
    chemin = "../data/"
    filename = "pluie"
    filename = chemin + filename
    generate_conll(text, filename)


    treebank_path = "../data/phrases_test.conll"
    corpus = grewpy.Corpus(treebank_path)
    param = "lemma"

    patterns = [
        # Tous les éléments présents
        """pattern {
            X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;
            Y-[det]->Z;
            X-[aux:pass|aux:tense]->W;
        }""",
        # Sans D1 (Z)
        """pattern {
            X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;
            X-[aux:pass|aux:tense]->W;
        }""",
        # Sans AUX (W)
        """pattern {
            X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;
            Y-[det]->Z;
        }""",
        # Sans D1 et AUX
        """pattern {
            X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;
        }""",
    ]

    all_matches = []
    for pat in patterns:
        req = grewpy.Request(pat)
        matches = corpus.search(req)
        all_matches.extend(matches)

    liste_enonces_elem = indexe_enonces_elem(corpus, all_matches, param)
    liste_enonces_elem = supprimer_doublons_semantiques(liste_enonces_elem)

    print("\n\nLISTE DES ÉNONCÉS ÉLÉMENTAIRES SANS DOUBLONS :\n")
    for element in liste_enonces_elem:
        print(element)




    # liste_des_enonces_elem=[]
    # n = 0

    # Un match est un X et un Y correspondant à la requête
    # match = {'sent_id': '3', 'matching': {'nodes': {'Y': '2', 'X': '4'}, 'edges': {}}}

    # for match in liste_match:
    #     n+= 1
    #     sent_id = match["sent_id"]
    #     print(f"sent_id = {sent_id}")

    #     # On récupère le numéro de node de Y et X
    #     #  {'nodes': {'Y': '2', 'X': '4'}}
    #     liste_node=[]
    #     for node_number in match["matching"]["nodes"].values():
    #         liste_node.append(int(node_number))
    #     liste_node.sort()
        
    #     # On récupère le 'param' demandé (ici 'lemma') pour chaque node
    #     liste_forms = []
    #     for node_number in liste_node:
    #         # print("corpus[sent_id].features", corpus[sent_id].features)
    #         if param in corpus[sent_id].features[str(node_number)]:
    #             # print(f"node_number = {node_number}")
    #             # print(f"param = {param}")
    #             # print(f"corpus[sent_id].features[str(node_number)] = {corpus[sent_id].features[str(node_number)]}")
                
    #             liste_forms.append(corpus[sent_id].features[str(node_number)][param])
    #     dico_un_enonce_elem = {
    #         "id_EE":n,
    #         "id_sent": sent_id,
    #         "formes": liste_forms,
    #     }
    #     liste_des_enonces_elem.append(dico_un_enonce_elem)
    # return liste_des_enonces_elem