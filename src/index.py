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
    print("liste_match", liste_match)
    
    liste_des_enonces_elem=[]
    n = 0

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

    for match in liste_match:
        n+=1
        sent_id= match["sent_id"]
        formes_EE = {
            "D1": corpus[sent_id].features[str(match["matching"]["nodes"]["Z"])]["lemma"],
            "N1": corpus[sent_id].features[str(match["matching"]["nodes"]["Y"])]["lemma"],
            "AUX": corpus[sent_id].features[str(match["matching"]["nodes"]["W"])]["lemma"],
            "V": corpus[sent_id].features[str(match["matching"]["nodes"]["X"])]["lemma"],

        }
        dico_un_enonce_elem = {
            "id_EE":n,
            "id_sent": sent_id,
            "formes_EE": formes_EE,
        }
        liste_des_enonces_elem.append(dico_un_enonce_elem)
    return liste_des_enonces_elem

    # X-->

if __name__ == "__main__":
    # Exemple d'utilisation
    treebank_path = "../data/phrases_test.conll"
    corpus = grewpy.Corpus(treebank_path)
    req = "pattern { X-[nsubj|obj|iobj|nsubj:pass|cop]->Y;" \
    "Y-[det]->Z;" \
    "X-[aux:pass|aux:tense]->W}"
    param = "lemma"
    liste_enonces_elem = indexe_enonces_elem(corpus, req, param)
    print("\n\nLISTE DES ÉNONCÉS ÉLÉMENTAIRES :\n\n",liste_enonces_elem, "\n\n")
    for element in liste_enonces_elem:
        print(element)

