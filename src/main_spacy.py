import spacy

# Charger le modèle français de SpaCy
nlp = spacy.load("fr_core_news_sm")

# Définition des relations selon le tableau fourni
relations_phi = {"mark", "cc", "advcl", "csubj", "ccomp", "xcomp", "acl"}  # Relations interpropositionnelles (connecteurs logiques)
relations_delta = {"nmod", "appos", "numod", "amod"}  # Relations intrapropositionnelles (modifieurs, compléments)

# Exemple de phrase à analyser
texte = "Le bois est plus léger que l'eau puisqu'il remonte à la surface lorsqu'on l'enfonce dans l'eau."

# Analyse du texte avec SpaCy
doc = nlp(texte)

# Liste des relations détectées
relations_detectees = []

# Parcourir les tokens du texte
for token in doc:
    relation = "rien"

    # Vérifier si la relation est une relation phi (uniquement pour les marqueurs logiques, pas les verbes)
    if token.dep_ in relations_phi and token.pos_ != "VERB":
        relation = "phi_" + token.dep_

    # Vérifier si la relation est une relation delta (intrapropositionnelle)
    elif token.dep_ in relations_delta:
        relation = "delta_" + token.dep_

    # Stocker le résultat uniquement si la relation est pertinente
    if relation != "rien":
        relations_detectees.append({"mot": token.text, "relation": relation, "gouverneur": token.head.text})

# 🔹 **Affichage des relations détectées**
print("\n🔹 **Relations détectées :**")
for relation in relations_detectees:
    print(f"Mot: {relation['mot']}  ➝ Relation: {relation['relation']}  ➝ Gouverneur: {relation['gouverneur']}")
