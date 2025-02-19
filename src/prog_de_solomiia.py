import stanza

def process_text(text, ud_mapping):
    nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma,depparse')
    doc = nlp(text)
    
    element_list = []
    id_counter = 1
    
    for sentence in doc.sentences:
        tokens = [word.lemma for word in sentence.words if word.deprel not in ["nmod", "obl", "advmod"]]
        base_entry = {
            "id": id_counter,
            "formes": tokens,
            "gouverneur": 0,
            "type de relation": "rien",
            "UD": "rien"
        }
        element_list.append(base_entry)
        
        for word in sentence.words:
            if word.deprel in ud_mapping:
                id_counter += 1
                dep_entry = {
                    "id": id_counter,
                    "formes": modify_sentence(tokens, word.id - 1),
                    "gouverneur": base_entry["id"],
                    "type de relation": ud_mapping[word.deprel],
                    "UD": word.deprel
                }
                element_list.append(dep_entry)
                
        id_counter += 1
    
    return element_list

def modify_sentence(tokens, index):
    new_tokens = tokens[:]
    new_tokens[index] = "Ø"  # Remplace l'élément à index par Ø
    return new_tokens

if __name__ == "__main__":
    text = "Le roi et la reine arrivent sur le trône. Le roi qui est anglais arrive sur le trône."
    ud_mapping = {"cc": "phi", "acl": "phi", "amod": "phi", "ccomp": "phi", "xcomp": "phi", "nsubj": "phi", "obj": "phi", "iobj": "phi"}  # Définition des relations UD et leurs types
    results = process_text(text, ud_mapping)
    
    for entry in results:
        print(entry)
