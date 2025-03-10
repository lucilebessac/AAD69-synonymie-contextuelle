from conllu import parse

# Charger un fichier CoNLL-U
with open("eau.conll", "r", encoding="utf-8") as f:
    data = f.read()

# Parser les phrases
sentences = parse(data)

liste_des_enonces_elem = []

dico_1_enonce_elem = {}

liste_core_arguments = ["nsubj", "obj", "iobj"]

liste_core_arguments_locale = []

liste_heads = []
n = 0

for sentence in sentences:
    n+=1
    for token in sentence:
        if token['deprel'] == 'root' and token['upos'] == 'VERB':
            liste_heads.append(token['id'])
            liste_core_arguments_locale.append(token['id'])

            id_head = token['id']
            for token in sentence:
                if token['head'] == id_head and token['deprel'] in liste_core_arguments:
                    liste_core_arguments_locale.append(token['id'])
        elif token['deprel'] == 'root' and token['upos'] == 'ADJ':
            liste_heads.append(token['id'])

            liste_core_arguments_locale.append(token['id'])

            id_head = token['id']
            for token in sentence:
                if token['head'] == id_head and token['deprel'] in liste_core_arguments or token['head'] == id_head and token['deprel'] == 'cop':
                    liste_core_arguments_locale.append(token['id'])
        elif token['upos'] == 'VERB':
            liste_heads.append(token['id'])

            liste_core_arguments_locale.append(token['id'])

            id_head = token['id']
            for token in sentence:
                if token['head'] == id_head and token['deprel'] in liste_core_arguments:
                    liste_core_arguments_locale.append(token['id'])

dico_1_enonce_elem = {
    "id": n,
    "core_args": liste_core_arguments_locale
}


print(dico_1_enonce_elem)


print (liste_core_arguments_locale)
print (liste_heads)


## BROUILLON
# for head in liste_heads:
#     for arg in liste_core_arguments_locale:

# x = 0
# for head in liste_heads:
#     x+=1
#     for sentence in sentences:
#         for token in sentence:
#             if token['head'] == head:
