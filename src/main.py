import stanza

# phrase = "Quand ils arrivèrent, le Roi et la Reine étaient assis sur des trônes. Une grande foule les entourait, composée de toutes sortes de quadrupèdes et d'oiseaux, et de tout le paquet de cartes. Le Valet de Coeur, debout devant eux, était enchaîné et encadré de deux soldats. Près du Roi se tenait le Lapin Blanc : il avait une trompette dans une main et dans l'autre un rouleu de parchemin. Sur une table au milieu de la salle était posé un grand plateau de tartes. Elles étaient si appétissantes qu'Alice eut une envie folle de les manger."
# phrase = "Pierre a un chien et Marie a un chat."
phrase = "Le bois est plus léger que l'eau puisqu'il remonte à la surface lorsqu'on l'enfonce dans l'eau."
# phrase = "Le roi et la reine arrivent sur le trône"


### Étape 1 : Stanza

# Initialisation de Stanza
nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma,depparse', download_method=None)

# Déclencheurs de rel phi et delta
declencheurs_phi = ["csubj", "ccomp", "xcomp","mark", "acl"] # Liste des dep qui déclenchent une relation phi
    # On exclut advcl pour l'instant car on ne sait pas le gérer
declencheurs_delta = ["nmod", "appos", "nummod", "amod"] # Liste des dep qui déclenchent une relation delta

# Traitement de la phrase avec Stanza
doc = nlp(phrase)

liste_enonces = []
enonce_courant = []

for i, sentence in enumerate(doc.sentences):
    print(f"\n========== Phrase {i+1} ==========\n")
    for word in sentence.words:

        # Afficher le mot, la relation de dépendance et le mot parent
        head_text = sentence.words[word.head - 1].text if word.head > 0 else "ROOT"
        print(f"{word.text} --> {word.deprel} --> {head_text}")
        
        enonce_courant.append(word.text) # On ajoute le mot courant

        ## On segmente si on trouve une rel phi
        if word.deprel in declencheurs_phi:
            print("----- relation phi détectée -----")
            liste_enonces.append(" ".join(enonce_courant)) # On ajoute le courant à la liste complète
            enonce_courant = [] #On réinitialise

        # elif word.deprel in declencheurs_delta:
        #     print("----- relation delta détectée -----")
        # else:
        #     None

    # Pour le dernier énoncé qu'il reste
    if enonce_courant:
        liste_enonces.append(" ".join(enonce_courant))
        enonce_courant = []

print("\n========== Liste des énoncés ==========\n")
for i, enonce in enumerate(liste_enonces, 1):
    print(f"E{i}: {enonce}")