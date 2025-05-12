import grewpy
from grewpy import Corpus, Request, Graph


def configuration():
    """
    Configuration de GrewPy.
    """
    # Configuration au format SUD
    grewpy.set_config("sud")

    ## Import data
    #Corpus est un fichier conllu ou un dossier qui en contient 
    # Sur un Corpus on peut faire des queries ou compter des occurences

    treebank_path = "../../data/phrases_test.conll"
    corpus = Corpus(treebank_path)
    print(f"Available sentence IDs: {corpus.get_sent_ids()}")
    return corpus

def requetes(corpus):
    """
    Queries sur le corpus.
    """
    n_sentences = len(corpus)
    sent_ids = corpus.get_sent_ids()

    print(f"n_sentences = {n_sentences}")
    print(f"sent_ids = {sent_ids}")

    # Example of a request to count the number of subjects in the corpus
    # The request is defined using a pattern
    # req_test = Request("pattern { X-[subj]->Y }")
    # corpus.count(req_test)

    req_mon_pattern2 = Request("pattern { X-[nsubj|obj|iobj|nsubj:pass]->Y}")

    # Perform the search and store the results
    resultats = corpus.search(req_mon_pattern2)

    return resultats

def extraire_graph(corpus, sent_id):
    """
    Extract the graph for a given sentence ID.
    """
    # Get the graph for the specified sentence ID
    graph = corpus[sent_id]

    # Print the graph
    print(f"Graph for sentence ID {sent_id}:")
    print(graph)

    return graph


if __name__ == "__main__":
    # Configuration
    corpus = configuration()

    # Perform queries
    resultats = requetes(corpus)

    # Print the results
    print("\n**Résultats de la requête**")
    print(resultats)

    # graph = extraire_graph(corpus, '1')
    
    # with open("../../data/pluie.svg", "w") as f:
    #     f.write(graph.to_svg(draw_root=True))
