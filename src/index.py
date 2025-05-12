#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 14:21:23 

Pour un Corpus (object GrewPy), une request et un parametre donné, donne les mots qu'il ya derrière
Grâce au numéro de node, on peut récupérer le mot correspondant dans le corpus
Grâce au module features

@author: hugodumoulin
"""

import grewpy

def indexe_enonces_elem(corpus, req, param):
    grewpy.set_config("sud")
    request = grewpy.Request(req)
    liste_match=corpus.search(request)
    liste_des_enonces_elem=[]
    n = 0
    for match in liste_match:
        n+= 1
        sent_id = match["sent_id"]
        print(f"sent_id = {sent_id}")
        ##on affiche le text de la phrase
        liste_node=[]
        for node_number in match["matching"]["nodes"].values():
            liste_node.append(int(node_number))
        liste_node.sort()
        liste_forms = []
        for node_number in liste_node:
            if param in corpus[sent_id].features[str(node_number)]:
                liste_forms.append(corpus[sent_id].features[str(node_number)][param])
        dico_un_enonce_elem = {
            "id":n,
            "sent_id": sent_id,
            "formes": liste_forms,
        }
        liste_des_enonces_elem.append(dico_un_enonce_elem)
    return liste_des_enonces_elem

if __name__ == "__main__":
    # Exemple d'utilisation
    treebank_path = "../data/phrases_test.conll"
    corpus = grewpy.Corpus(treebank_path)
    req = "pattern { X-[nsubj|obj|iobj|nsubj:pass|cop]->Y }"
    param = "lemma"
    liste_enonces_elem = indexe_enonces_elem(corpus, req, param)
    print(liste_enonces_elem)
    for element in liste_enonces_elem:
        print(element)

