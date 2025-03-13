import spacy

# Charger le modèle français de Spacy
nlp = spacy.load("fr_core_news_sm")

def analyse_dependance(texte):
    # Analyser le texte avec Spacy
    doc = nlp(texte)
    
    # Affichage des relations de dépendance
    print("🔍 **Relations de dépendance** (TOKEN | DEP | HEAD)")
    for token in doc:
        print(f"{token.text} | {token.dep_} | {token.head.text}")

    # Extraire les arguments nominaux
    sujets = []
    objets_directs = []
    objets_indirects = []
    prepositions = []
    
    for token in doc:
        if token.dep_ == "nsubj":
            sujets.append(token.text)
        elif token.dep_ == "obj":
            objets_directs.append(token.text)
        elif token.dep_ == "iobj":
            objets_indirects.append(token.text)
        elif token.dep_ == "case":
            prepositions.append(token.text)
    
    print("\n📝 **Arguments nominaux extraits**")
    print(f"Sujets: {sujets}")
    print(f"Objets directs: {objets_directs}")
    print(f"Objets indirects: {objets_indirects}")
    print(f"Prépositions: {prepositions}")
    
    # Extraire les propositions
    propositions = extraire_propositions(doc)
    
    print("\n🔎 **Propositions extraites**")
    for prop in propositions:
        print(f"- {prop}")

def extraire_propositions(doc):
    propositions = []
    
    for sent in doc.sents:
        sujet = ""
        verbe = ""
        complement = ""
        preposition = ""
        
        for token in sent:
            # Identifier le sujet
            if token.dep_ == "nsubj":
                sujet = token.text
            # Identifier le verbe (root)
            elif token.dep_ == "ROOT":
                verbe = token.text
            # Identifier les compléments (objets)
            elif token.dep_ == "obj":
                complement = token.text
            # Identifier les prépositions et les objets indirects
            elif token.dep_ == "case":
                preposition = token.text
        
        # Formuler une proposition
        if sujet and verbe:
            proposition = f"{sujet} {verbe}"
            if complement:
                proposition += f" {complement}"
            if preposition:
                proposition += f" {preposition}"
            propositions.append(proposition)
    
    return propositions

# Exemple de texte d'entrée
texte = "Le chat mange la souris sous la table."

# Lancer l'analyse
analyse_dependance(texte)
