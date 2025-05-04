import grewpy
from grewpy import Corpus, Request, Graph


def configuration():
    """
    Set the configuration for GrewPy.
    """
    # Set the configuration to use the Universal Dependencies (UD) format
    # This is important for parsing and analyzing the corpus correctly
    # The configuration can be set to "sud" or "ud" depending on the corpus format
    grewpy.set_config("sud")

    ## Import data

    #The Corpus constructor takes a conllu file or a directory containing conllu files. 
    # #A Corpus allows to make queries and to count occurrences.

    treebank_path = "../../data/pluie.conll"
    corpus = Corpus(treebank_path)
    print(f"Available sentence IDs: {corpus.get_sent_ids()}")
    return corpus

def requetes(corpus):
    """
    Perform queries on the corpus.
    """
    n_sentences = len(corpus)
    sent_ids = corpus.get_sent_ids()

    print(f"n_sentences = {n_sentences}")
    print(f"sent_ids[0] = {sent_ids[0]}")

    # Example of a request to count the number of subjects in the corpus
    # The request is defined using a pattern
    req_test = Request("pattern { X-[subj]->Y }")
    corpus.count(req_test)

    # print the lemma of the items that are either nsubj, obj or iobj
    req_mon_pattern = Request().pattern("X-[nsubj|obj|iobj]->Y ")
    req_mon_pattern2 = Request("pattern X-[nsubj|obj|iobj]->Y ")

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
    # resultats = requetes(corpus)

    # # Print the results
    # print("\n🔎 **Résultats de la requête**")
    # print(resultats)

    graph = extraire_graph(corpus, '1')
    
    with open("../../data/pluie.svg", "w") as f:
        f.write(graph.to_svg(draw_root=True))
