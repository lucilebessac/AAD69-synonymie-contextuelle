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

def index(corpus, req, param):
    grewpy.set_config("sud")
    request = grewpy.Request(req)
    liste_match=corpus.search(request)
    index=[]
    for match in liste_match:
        sent_id = match["sent_id"]
        liste_node=[]
        for node_number in match["matching"]["nodes"].values():
            liste_node.append(int(node_number))
        liste_node.sort()
        liste_forms = []
        for node_number in liste_node:
            if param in corpus[sent_id].features[str(node_number)]:
                liste_forms.append(corpus[sent_id].features[str(node_number)][param])
        index.append(liste_forms)
    return index