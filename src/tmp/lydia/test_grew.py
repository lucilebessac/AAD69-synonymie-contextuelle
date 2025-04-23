from grewpy import Corpus, Request
import grewpy

grewpy.set_config("sud")

# Chemin vers le corpus
treebank_path = "SUD_English-PUD/en_pud-sud-test.conllu"
corpus = Corpus(treebank_path)

print(f"✅ Corpus chargé : {len(corpus)} phrases trouvées.")
