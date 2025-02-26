import spacy

# Modèle
nlp = spacy.load("fr_core_news_md")

# Phrase
phrase = "Le bois est plus léger que l'eau puisqu'il remonte à la surface lorsqu'on l'enfonce dans l'eau."

# Analyse du texte avec SpaCy
doc = nlp(phrase)

# Dico des nominals core arguments
nom_core_arguments = {
    "nsubj": [],
    "obj": [],
    "iobj": []
}

# Extraire les core arguments / nominals
def extract_nominal_core_arguments(doc):
    # Dictionnaire local pour stocker les résultats
    local_core_args = {
        "nsubj": [],
        "obj": [],
        "iobj": []
    }
    
    # Afficher toutes les dépendances
    print("TOUTES LES DÉPENDANCES:")
    print(f"{'TOKEN':<10} {'DEP':<10} {'HEAD':<10}")
    print("-" * 50)
    
    # Afficher le token et si il est un core argument, le stocker
    for token in doc:
        print(f"{token.text:<10} {token.dep_:<10} {token.head.text:<10}")
        if token.dep_ in local_core_args:
            local_core_args[token.dep_].append({
                "token": token.text,
                "token_position": token.i,
                "head": token.head.text,
                "head_position": token.head.i,
                "relation": token.dep_
            })
    
    return local_core_args

# Nouvelle fonction pour extraire et reconstruire la structure de base de chaque proposition
def extraire_structure_de_base(doc):
    # Dictionnaire pour stocker les structures de base de chaque proposition
    propositions = []
    
    # Identifier les verbes principaux (racines ou verbes connectés par des marqueurs de subordination)
    verbes_principaux = []
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == "VERB":
            verbes_principaux.append(token)
        # Trouver d'autres verbes principaux dans les propositions subordonnées
        elif token.pos_ == "VERB" and token.dep_ in ["conj", "ccomp", "xcomp", "advcl"]:
            verbes_principaux.append(token)
    
    # Pour chaque verbe principal, trouver ses arguments
    for verbe in verbes_principaux:
        structure = {
            "verbe": verbe,
            "sujet": None,
            "objet": None,
            "objet_indirect": None
        }
        
        # Chercher les arguments directement liés au verbe
        for token in doc:
            if token.head == verbe:
                if token.dep_ == "nsubj":
                    # Récupérer le groupe nominal complet (avec les déterminants, adjectifs, etc.)
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["sujet"] = doc[start_idx:end_idx]
                
                elif token.dep_ == "obj":
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["objet"] = doc[start_idx:end_idx]
                
                elif token.dep_ == "iobj":
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["objet_indirect"] = doc[start_idx:end_idx]
        
        # Chercher les sujets possiblement éloignés (pronoms, etc.)
        if not structure["sujet"]:
            for token in doc:
                if token.dep_ == "nsubj" and token.head.i <= verbe.i <= token.head.i + 5:
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["sujet"] = doc[start_idx:end_idx]
                    break
        
        # Ajouter la structure si elle contient au moins un verbe et un sujet
        if structure["sujet"]:
            propositions.append(structure)
    
    # Reconstruire les phrases simplifiées
    phrases_simplifiees = []
    for prop in propositions:
        phrase = str(prop["sujet"]) + " " + prop["verbe"].text
        if prop["objet"]:
            phrase += " " + str(prop["objet"])
        if prop["objet_indirect"]:
            phrase += " " + str(prop["objet_indirect"])
        phrases_simplifiees.append(phrase)
    
    return phrases_simplifiees, propositions

# Extraire les core arguments comme avant
results = extract_nominal_core_arguments(doc)

# Afficher les nom core arguments trouvés
print("\nLES NOMINAL CORE ARGUMENTS TROUVÉS:")
print("-" * 50)
for relation_type, arguments in results.items():
    if arguments:
        print(f"\n{relation_type.upper()} (nb: {len(arguments)}):")
        for arg in arguments:
            print(f" - '{arg['token']}' -- {arg['relation']} --> '{arg['head']}'")
    else:
        print(f"\n{relation_type.upper()}: -")

# Afficher les dépendances avec les nom core arguments mis en avant
print("\nLA PHRASE ET LES NOMINAL CORE ARGUMENTS TROUVÉS:")
print("-" * 50)
for token in doc:
    # Highlight core arguments
    if token.dep_ in ["nsubj", "obj", "iobj"]:
        print(f"{token.i}: {token.text:<15} --{token.dep_}--> {token.head.text} (Position: {token.head.i})")
    else:
        print(f"{token.i}: {token.text:<15} {token.dep_}")

# Appliquer la nouvelle fonction pour extraire la structure de base
print("\nSTRUCTURE DE BASE DE LA PHRASE:")
print("-" * 50)
phrases_simples, structures = extraire_structure_de_base(doc)

print("Phrase originale:")
print(phrase)
print("\nPropositions simplifiées:")
for i, simple in enumerate(phrases_simples, 1):
    print(f"{i}. {simple}")

print("\nDétail des structures extraites:")
for i, struct in enumerate(structures, 1):
    print(f"\nProposition {i}:")
    print(f"  Verbe: {struct['verbe'].text}")
    print(f"  Sujet: {struct['sujet'] if struct['sujet'] else '-'}")
    print(f"  Objet direct: {struct['objet'] if struct['objet'] else '-'}")
    print(f"  Objet indirect: {struct['objet_indirect'] if struct['objet_indirect'] else '-'}")