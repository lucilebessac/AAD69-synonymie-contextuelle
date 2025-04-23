import grewpy
from grewpy import Corpus, Request

grewpy.set_config("ud")

## Import data

#The Corpus constructor takes a conllu file or a directory containing conllu files. 
# #A Corpus allows to make queries and to count occurrences.

treebank_path = "../../data/pluie.conll"
corpus = Corpus(treebank_path)
print(type(corpus))

n_sentences = len(corpus)
sent_ids = corpus.get_sent_ids()

print(f"n_sentences = {n_sentences}")
print(f"sent_ids[0] = {sent_ids[0]}")


# Count the number of subjets in the corpus
req_test = Request("pattern { X-[subj]->Y }")
corpus.count(req_test)

# print the lemma of the items that are either nsubj, obj or iobj
req_mon_pattern = Request().pattern("X-[nsubj|obj|iobj]->Y ")
req_mon_pattern2 = Request("pattern X-[nsubj|obj|iobj]->Y ")

resultats = corpus.search(req_mon_pattern2)

print(resultats)



