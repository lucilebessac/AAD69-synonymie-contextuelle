import spacy

def process_text(text, ud_mapping):
    nlp = spacy.load("fr_core_news_md")
    doc = nlp(text)
    
    element_list = []
    id_counter = 1
    
    for sent in doc.sents:
        tokens = [token.lemma_ for token in sent if token.dep_ not in ["nmod", "obl", "advmod"]]
        base_entry = {
            "id": id_counter,
            "formes": tokens,
            "gouverneur": 0,
            "type de relation": "rien",
            "UD": "rien"
        }
        element_list.append(base_entry)
        
        for token in sent:
            if token.dep_ in ud_mapping:
                id_counter += 1
                dep_entry = {
                    "id": id_counter,
                    "formes": modify_sentence(tokens, token.i),
                    "gouverneur": base_entry["id"],
                    "type de relation": ud_mapping[token.dep_],
                    "UD": token.dep_
                }
                element_list.append(dep_entry)
                
        id_counter += 1
    
    return element_list

def modify_sentence(tokens, index):
    new_tokens = tokens[:]
    if 0 <= index < len(new_tokens):
        new_tokens[index] = "Ø"  # Remplace l'élément à l'index par Ø
    return new_tokens

if __name__ == "__main__":
    text = "Le roi et la reine arrivent sur le trône. Le roi qui est anglais arrive sur le trône."
    ud_mapping = {"cc": "phi", "acl": "phi", "amod": "phi", "ccomp": "phi", "xcomp": "phi", "nsubj": "phi", "obj": "phi", "iobj": "phi"}  # Définition des relations UD et leurs types
    results = process_text(text, ud_mapping)
    
    for entry in results:
        print(entry)