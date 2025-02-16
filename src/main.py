import stanza

phrase = "Quand ils arrivèrent, le Roi et la Reine étaient assis sur des trônes. Une grande foule les entourait, composée de toutes sortes de quadrupèdes et d'oiseaux, et de tout le paquet de cartes. Le Valet de Coeur, debout devant eux, étaiet enchaîné et encadré de deux soldats. Près du Roi se tenait le Lapin Blanc : il avait une trompette dans une main et dans l'autre un rouleu de parchemin. Sur une table au milieu de la salle était posé un grand plateau de tartes. Elles étaient si appétissantes qu'Alice eut une envie folle de les manger."
# phrase = "Pierre a un chien et Marie a un chat."

## Étape 1 : utiliser Stanza pour extraire les deprels

# Initialisation de Stanza
nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma,depparse', download_method=None)

# Traitement de la phrase

doc = nlp(phrase)

# Affichage des dépendances

declencheurs_phi = ["csubj", "ccomp", "xcomp", "obl", "advmod", "discourse", "nmod", "appos", "nummod", "acl", "amod"]

for i, sentence in enumerate(doc.sentences):
    print(f"Phrase {i+1}")
    for word in sentence.words:
        head_text = sentence.words[word.head - 1].text if word.head > 0 else "ROOT"
        print(f"{word.text} --> {word.deprel} --> {head_text}")
        ## si word.deprel = scubj ou ccomp ou xcomp alors print "relation phi"
        if word.deprel in declencheurs_phi:
            print("---------- relation phi détectée ----------")
