import torch
import torch.serialization
from numpy.core.multiarray import _reconstruct

# Pour gérer l'erreur Pytorch / STanza 
torch.serialization.add_safe_globals([_reconstruct])

# Problème sur la fonction torch.load / weights_only=False
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# On peut passer à notre fonction conll
import os
import pandas as pd
from spacy_conll import init_parser

# Script qui génère le conll d'un texte avec spacy-conll
nlp = init_parser("fr",
                "stanza",
                parser_opts={"use_gpu": True, "verbose": False},
                include_headers=True)

phrase = "Le bois est plus léger que l'eau puisqu'il flotte lorsqu'on l'enfonce dans l'eau."
doc = nlp(phrase)

# sauvegarder au format .conll
conll = doc._.conll_str
with open("eau.conll", "w", encoding="utf-8") as f:
    f.write(conll)


conll_df = doc._.conll_pd
conll_df.to_csv("eau.csv", sep="\t", index=False)

#  sauvegarder le con