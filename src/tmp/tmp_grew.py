import grewpy
from grewpy import Corpus, Request

grewpy.set_config("sud")

treebank_path = "en_pud-sud-test.conllu"
corpus = Corpus(treebank_path)