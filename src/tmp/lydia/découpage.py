import spacy

# Charger le modèle français de SpaCy
nlp = spacy.load("fr_core_news_sm")

# Définition des relations selon le tableau fourni
relations_phi = {"mark", "cc", "advcl", "csubj", "ccomp", "xcomp", "acl"}  # Relations interpropositionnelles (connecteurs logiques)
relations_delta = {"nmod", "appos", "numod", "amod"}  # Relations intrapropositionnelles (modifieurs, compléments)
relations_core = {"nsubj", "obj", "iobj"}  # Éléments principaux pour les énoncés élémentaires

# Exemple de phrase à analyser
texte = "Le bois est plus léger que l'eau puisqu'il remonte à la surface lorsqu'on l'enfonce dans l'eau."

# Analyse du texte avec SpaCy
doc = nlp(texte)

# Liste des relations détectées
relations_detectees = []
segments = []
segment_courant = []
dernier_sujet = None
dernier_verbe = None

# Parcourir les tokens du texte
for token in doc:
    relation = "rien"

    # Vérifier si la relation est une relation phi (connecteurs logiques)
    if token.dep_ in relations_phi and token.pos_ != "VERB":
        relation = "phi_" + token.dep_

        # Fermer le segment courant et ajouter à la liste des énoncés
        if segment_courant:
            segments.append(segment_courant)

        # Démarrer un nouveau segment avec le sujet et verbe conservés
        segment_courant = [dernier_sujet] if dernier_sujet else []
        if dernier_verbe and dernier_verbe not in segment_courant:
            segment_courant.append(dernier_verbe)

        continue  # Ne pas inclure le connecteur Phi

    # Vérifier si la relation est une relation delta (intrapropositionnelle)
    elif token.dep_ in relations_delta:
        relation = "delta_" + token.dep_

    # Stocker la relation détectée
    relations_detectees.append({"mot": token.text, "relation": relation, "gouverneur": token.head.text})

    # Sauvegarder le dernier sujet et verbe
    if token.dep_ in {"nsubj", "nsubj:pass"}:
        dernier_sujet = token.text
    if token.pos_ == "VERB":
        dernier_verbe = token.text

    # Ajouter le mot au segment courant
    segment_courant.append(token.text)

# Ajouter le dernier segment s'il en reste un
if segment_courant:
    segments.append(segment_courant)

# 🔹 **Affichage des relations détectées**
print("\n🔹 **Relations détectées :**")
for relation in relations_detectees:
    print(f"Mot: {relation['mot']}  ➝ Relation: {relation['relation']}  ➝ Gouverneur: {relation['gouverneur']}")

# 🔹 **Affichage des énoncés élémentaires générés**
print("\n🔹 **Énoncés Élémentaires :**")
for i, segment in enumerate(segments, start=1):
    print(f"E{i}: {' '.join([mot for mot in segment if mot is not None])}")
