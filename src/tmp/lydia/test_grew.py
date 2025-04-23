from grewpy import Corpus, Request
import grewpy

# Configurer GrewPy pour le format SUD
grewpy.set_config("sud")

# Chemin vers le corpus
treebank_path = "../../../data/SUD_English-PUD/en_pud-sud-test.conllu"
corpus = Corpus(treebank_path)

# Infos générales
n_sentences = len(corpus)
sent_ids = corpus.get_sent_ids()

print(f"✅ Corpus chargé : {n_sentences} phrases trouvées.")
print(f"🆔 ID de la première phrase : {sent_ids[0]}")

# Requête 1 : relation générique 'subj'
req_subj = Request("pattern { X-[subj]->Y }")
count_subj = corpus.count(req_subj)
print(f"\n🔍 Nombre de correspondances pour 'subj' : {count_subj}")

# Requête 2 : relation 'nsubj'
req_nsubj = Request("pattern { X-[nsubj]->Y }")
matches_nsubj = corpus.search(req_nsubj)
print(f"🔍 Nombre de correspondances pour 'nsubj' : {len(matches_nsubj)}")

print("\n📌 Exemples de correspondances 'nsubj' :\n")
for i, match in enumerate(matches_nsubj[:5]):
    print(f"➡️  Match {i+1}")
    for var, node_id in match.items():
        graph_id = sent_ids[0]  # ⚠️ c’est une simplification (prend la 1ère phrase)
        graph = corpus.get_graph(graph_id)
        form = graph.get_node_attr(node_id, "form")
        upos = graph.get_node_attr(node_id, "upos")
        print(f"   {var} ➝ {form} ({upos})")
    print("-" * 30)



# Requête 3 : Comptage des relations 'subj' groupées par type grammatical du sujet
req5 = Request("pattern { X-[subj]->Y }")
clusters = corpus.count(req5, clustering_parameter=["X.upos"])

print("\n📊 Répartition des relations 'subj' selon la catégorie grammaticale du sujet :\n")
for upos, count in clusters.items():
    print(f" - {upos} ➝ {count} occurences")
