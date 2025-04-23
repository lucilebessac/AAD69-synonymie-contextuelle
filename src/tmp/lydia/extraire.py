import pandas as pd

def extraire_heads_et_core_arguments(fichier_csv):
    """
    Extrait les prédicats principaux et leurs core arguments à partir d'un fichier CoNLL CSV.
    Chaque entrée aura un ID unique et contiendra la forme du HEAD.

    :param fichier_csv: Chemin du fichier CSV
    :return: Liste des prédicats avec leurs core arguments sous forme de dictionnaire
    """
    # Charger le fichier CSV
    df = pd.read_csv(fichier_csv, sep=None, engine='python')  # Auto-détecter le séparateur

    # Vérifier si les colonnes nécessaires sont présentes
    if not {"HEAD", "DEPREL", "UPOS", "FORM", "ID"}.issubset(df.columns):
        print("❌ Erreur : Colonnes nécessaires ('HEAD', 'DEPREL', 'UPOS', 'FORM', 'ID') manquantes.")
        return []

    # Étape 1 : Identification des prédicats principaux
    conditions_predicats = (
        (df["UPOS"] == "VERB") |  # Tous les VERB doivent être pris
        ((df["UPOS"].isin(["ADJ", "NOUN"])) & (df["DEPREL"].isin(["ROOT", "conj", "ccomp", "xcomp", "advcl"])))  # Adjectifs/Noms avec copule
    )

    # Liste des ID qui sont des prédicats principaux
    heads_predicats = df.loc[conditions_predicats, "ID"].dropna().astype(int).unique().tolist()
    print(heads_predicats)
    
    # Étape 2 : Extraction des core arguments liés aux prédicats
    core_arguments = {}
    id_counter = 1  # Initialisation de l'ID unique

    for _, row in df.iterrows():
        head_id = row["HEAD"]  # Numéro du gouverneur
        dep = row["DEPREL"]  # Relation syntaxique
        form = row["FORM"]  # Mot correspondant

        # Vérifier si le HEAD fait partie des prédicats principaux
        if head_id in heads_predicats:
            # Récupérer la forme du HEAD en utilisant son ID
            head_form = df.loc[df["ID"] == head_id, "FORM"].values
            head_form = head_form[0] if len(head_form) > 0 else None  # Éviter les erreurs si HEAD est absent

            if head_id not in core_arguments:
                core_arguments[head_id] = {
                    "id": id_counter,  # Associer un ID unique
                    "head": head_form,  # Ajouter la **forme du HEAD** dans le dictionnaire
                    "nsubj": [],
                    "obj": [],
                    "iobj": []
                }
                id_counter += 1  # Incrémenter l'ID

            # Ajouter les arguments selon la relation
            if dep == "nsubj":
                core_arguments[head_id]["nsubj"].append(form)
            elif dep == "obj":
                core_arguments[head_id]["obj"].append(form)
            elif dep == "iobj":
                core_arguments[head_id]["iobj"].append(form)

    return heads_predicats, core_arguments

# Exemple d'utilisation
fichier_csv = "eau.csv"  # Mets ici le bon chemin de ton fichier
heads_predicats, core_args = extraire_heads_et_core_arguments(fichier_csv)

# Affichage des résultats
print("\n🔹 **Liste des HEADs correspondant aux prédicats principaux :**")
print(heads_predicats)

print("\n🔹 **Core Arguments extraits avec ID unique et FORME du HEAD :**")
for head, args in core_args.items():
    print(f"HEAD '{args['head']}': {args}")

