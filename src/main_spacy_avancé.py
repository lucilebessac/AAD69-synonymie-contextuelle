import spacy

# Modèle
nlp = spacy.load("fr_core_news_md")

# Phrase
phrase = "Le bois est plus léger que l'eau puisqu'il remonte à la surface lorsqu'on l'enfonce dans l'eau."
# phrase = "Le roi qui est anglais arrive sur le trône avec sa soeur."

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
    local_core_args = {
        "nsubj": [],
        "obj": [],
        "iobj": []
    }
    
    # Afficher toutes les dépendances
    print("TOUTES LES DÉPENDANCES:")
    print(f"{'TOKEN':<12} {'DEP':<10} {'HEAD':<12}")
    print("-" * 50)
    
    # Afficher le token et si il est un core argument, le stocker
    for token in doc:
        print(f"{token.text:<12} {token.dep_:<10} {token.head.text:<12}")
        if token.dep_ in local_core_args:
            local_core_args[token.dep_].append({
                "token": token.text,
                "token_position": token.i,
                "head": token.head.text,
                "head_position": token.head.i,
                "relation": token.dep_
            })
    
    return local_core_args

# Extraire et reconstruire la structure de base de chaque proposition
def extraire_structure_de_base(doc):
    # Dictionnaire pour stocker les structures de base de chaque proposition
    propositions = []
    
    # Identifier les prédicats principaux (verbes ou adjectifs/noms avec copule)
    predicats_principaux = []
    for token in doc:
        # Verbe racine
        if token.dep_ == "ROOT":
            if token.pos_ == "VERB":
                predicats_principaux.append({"type": "verb", "token": token})
            # Adjectif ou nom qui est racine (avec copule)
            elif token.pos_ in ["ADJ", "NOUN"]:
                # Chercher la copule associée
                copule = None
                for enfant in token.children:
                    if enfant.dep_ == "cop":
                        copule = enfant
                        break
                
                if copule:
                    predicats_principaux.append({"type": "cop", "token": token, "copule": copule})
        
        # Autres verbes principaux dans les propositions subordonnées
        elif token.pos_ == "VERB" and token.dep_ in ["conj", "ccomp", "xcomp", "advcl"]:
            predicats_principaux.append({"type": "verb", "token": token})
        
        # Adjectifs ou noms avec copule dans des propositions subordonnées
        elif token.pos_ in ["ADJ", "NOUN"] and token.dep_ in ["conj", "ccomp", "xcomp", "advcl"]:
            # Chercher la copule associée
            copule = None
            for enfant in token.children:
                if enfant.dep_ == "cop":
                    copule = enfant
                    break
            
            if copule:
                predicats_principaux.append({"type": "cop", "token": token, "copule": copule})
    
    # Pour chaque prédicat principal, trouver ses arguments
    for predicat in predicats_principaux:
        structure = {
            "predicat": predicat,
            "sujet": None,
            "objet": None,
            "objet_indirect": None
        }
        
        # Le token principal dépend du type de prédicat
        token_principal = predicat["token"]
        
        # Chercher les arguments directement liés au prédicat
        for token in doc:
            if token.head == token_principal:
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
        
        # Si c'est une structure copulaire, chercher aussi le sujet lié à la copule
        if predicat["type"] == "cop" and not structure["sujet"]:
            copule = predicat["copule"]
            for token in doc:
                if token.head == copule and token.dep_ == "nsubj":
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["sujet"] = doc[start_idx:end_idx]
        
        # Chercher les sujets possiblement éloignés (pronoms, etc.)
        if not structure["sujet"]:
            for token in doc:
                if token.dep_ == "nsubj" and token.head.i <= token_principal.i <= token.head.i + 5:
                    subtree = list(token.subtree)
                    start_idx = subtree[0].i
                    end_idx = subtree[-1].i + 1
                    structure["sujet"] = doc[start_idx:end_idx]
                    break
        
        # Ajouter la structure si elle contient au moins un prédicat et un sujet
        if structure["sujet"]:
            propositions.append(structure)
    
    # Reconstruire les phrases simplifiées
    phrases_simplifiees = []
    for prop in propositions:
        # Construction différente selon le type de prédicat
        if prop["predicat"]["type"] == "verb":
            phrase = str(prop["sujet"]) + " " + prop["predicat"]["token"].text
        else:  # type cop
            phrase = str(prop["sujet"]) + " " + prop["predicat"]["copule"].text + " " + prop["predicat"]["token"].text
        
        if prop["objet"]:
            phrase += " " + str(prop["objet"])
        if prop["objet_indirect"]:
            phrase += " " + str(prop["objet_indirect"])
        
        phrases_simplifiees.append(phrase)
    
    return phrases_simplifiees, propositions

# Extraire les core arguments
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

# Extraire la structure de base
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
    if struct["predicat"]["type"] == "verb":
        print(f"  Prédicat: {struct['predicat']['token'].text} (verbe)")
    else:
        print(f"  Prédicat: {struct['predicat']['copule'].text} {struct['predicat']['token'].text} (copule + complément)")
    print(f"  Sujet: {struct['sujet'] if struct['sujet'] else '-'}")
    print(f"  Objet direct: {struct['objet'] if struct['objet'] else '-'}")
    print(f"  Objet indirect: {struct['objet_indirect'] if struct['objet_indirect'] else '-'}")