import mistletoe
import re
from pathlib import Path
from textwrap import dedent
from mistletoe.block_token import Heading


SHORTCUT = "!!"
FILE = "testmark.md"
OUTPUT_FILE = "output.html"

def CenterText(md_content, New_file):
    found = False  # Variable globale pour suivre l'état de la recherche du motif
    # Ouverture du document Markdown en mode lecture pour inspection initiale
    #print(md_content)
    lines = md_content.splitlines('\n')
    print(lines)

    # Ouverture du document Markdown en mode écriture pour modification
    New_Doc = open(New_file, "w")
    for Symbol in lines:
        Shortcut = '()'  # Recherche du motif à remplacer
        if Symbol.find(Shortcut) != -1 and (found == False): # -1 signifie que le motif n'a pas été trouvé
            Symbol = Symbol.replace(Shortcut, '<div align="center">\n', 1) # Remplacement des balises Markdown par des balises HTML    
            # add an empty line
            found = True  # Indique que le motif a été trouvé et remplacé

        elif Symbol.find(Shortcut) != -1 and (found == True): # -1 signifie que le motif n'a pas été trouvé
            Symbol = Symbol.replace(Shortcut, '</div>\n', 1) # Remplacement des balises Markdown par des balises HTML
            found = False

        New_Doc.write(Symbol)
    New_Doc.close()
    # Envoie du document Markdown modifié à la fonction de rendu HTML
    with open(New_file, 'r') as fin:
        rendered = mistletoe.markdown(fin)  
        print(rendered)
        fin.close()

    with open(New_file, 'r') as fin:
        output =  fin.readlines()
        return ''.join(output)

    # Écriture du rendu HTML dans un fichier de sortie
    with open('Exemple.html', 'w') as fout:
        fout.write(rendered)
        fout.close()


def creer_table_matiere(fichier):

    # Lire le fichier
    with open(fichier, "r", encoding="utf-8") as f:
        texte = f.read()

    # Vérifier si le marqueur existe
    if "**contenu:**" not in texte.lower():
        print("Aucun **contenu:** détecté.")
        return

    print("**contenu:** détecté.")

    table = "## Table des matières\n\n"

    # Parser le document
    document = mistletoe.Document(texte)

    for element in document.children:

        if isinstance(element, Heading):

            if element.level == 2 or element.level == 3 or element.level == 4 or element.level == 5 or element.level == 6:

                titre = ""

                for enfant in element.children:
                    if hasattr(enfant, "content"):
                        titre += enfant.content

                lien = titre.lower().replace(" ", "-")

                # Ajouter le titre dans la table
                if element.level == 1:
                    table += f"- [{titre}](#{lien})\n"

                elif element.level == 2:
                    table += f"  - [{titre}](#{lien})\n"

                elif element.level == 3:
                    table += f"    - [{titre}](#{lien})\n"

                elif element.level == 4:
                    table += f"      - [{titre}](#{lien})\n"

                elif element.level == 5:
                    table += f"        - [{titre}](#{lien})\n"

                elif element.level == 6:
                    table += f"          - [{titre}](#{lien})\n"

    # Insérer la table après le marqueur
    texte = texte.replace(
        "**contenu:**",
        "" + table,
        1
    )

    # Sauvegarder
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(texte)

    print("Table des matières créée.")


def checklistMD_from_string(md_content):
    """
    Cette fonction transforme les lignes commençant par / dans une chaîne Markdown
    en cases à cocher HTML, puis convertit le tout en HTML.
    
    Args:
        md_content (str): Le contenu textuel au format Markdown
        
    Returns:
        str: Le contenu converti en HTML
    """
    modifiedLines = []
    
    # On sépare la chaîne en lignes individuelles
    lines = md_content.splitlines()

    for line in lines:
        # On vérifie si la ligne commence par "/"
        if line.strip().startswith('/'):
            # On retire le "/" et les espaces superflus autour du texte
            clean_text = line.strip().lstrip('/')
            
            # On crée la structure HTML pour la checkbox
            new_line = f'<input type="checkbox"> <label>{clean_text}</label><br>'
            modifiedLines.append(new_line)
        else if line.strip().startswith('\\'):
            # On retire le "\" et les espaces superflus autour du texte
            clean_text = line.strip().lstrip('\\')

            # On crée la structure HTML pour la checkbox
            new_line = f'<input type="checkbox" checked> <label>{clean_text}</label><br>'
            modifiedLines.append(new_line)
        else:
            # Si la ligne ne commence pas par "/" ou "\", on la laisse intacte
            modifiedLines.append(line)

    # On rassemble les lignes avec un saut de ligne
    modified_content = "\n".join(modifiedLines)

    # Conversion du Markdown modifié en HTML
    rendered = mistletoe.markdown(modified_content)
    
    return modified_content


def build_tree(path : str, max_depth, current_depth=1) -> dict | list | str:
    """
    Reads a folder and builds a tree consisting of all the files at a certain depth.
    """
    # Conversion de sécurité si max_depth est passé sous forme de chaîne
    max_depth = int(max_depth)

    if path in [r'\\', r'\\'[0]]:
        path = r''
    path = Path(path)
    
    if path.is_file(): 
        return path.name
        
    if current_depth == max_depth: 
        return [f.name for f in path.iterdir() if not f.name.startswith('.')]
        
    tree = {}
    for item in path.iterdir():
        if item.name.startswith('.'): 
            continue
            
        if item.is_dir(): 
            tree[item.name] = build_tree(item, max_depth, current_depth + 1)
        else:
            tree[item.name] = item.name
            
    return tree

def build_html(tree: dict | list | str) -> str:
    """
    Builds the html tree fragments
    """
    html = ''
    
    if isinstance(tree, list):
        for item in tree:
            html += f'<li><span class="file">{item}</span></li>' 

    elif isinstance(tree, str):
        html += f'<li><span class="file">{tree}</span></li>' 

    elif isinstance(tree, dict):
        for folder_name, content in tree.items():
            if isinstance(content, list):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content)
                html += '</ul></li>'
            elif isinstance(content, str):
                html += f'<li><span class="file">{content}</span></li>' 
            elif isinstance(content, dict):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content)
                html += '</ul></li>'
    return html

def render_tree_block(tree_dict):
    """
    Génère uniquement le bloc conteneur de l'arbre (SANS structure html complète)
    """
    corps_arbre = build_html(tree_dict) 
    
    return f'<div class="file-tree"><ul>{corps_arbre}</ul></div>'




if __name__ == "__main__":


    creer_table_matiere(FILE)

    with open(FILE, "r", encoding="utf-8") as fin:
        markdown_lines = fin.readlines()
        
    processed_lines = []
    for line in markdown_lines:
        if line.startswith(SHORTCUT):
            parameters = line[len(SHORTCUT):].strip().split(' ')
            path = parameters[0]
            
            try:
                depth = int(parameters[1])
            except (IndexError, ValueError):
                depth = 1
                
            
            tree_data = build_tree(path, depth)
            html_tree = render_tree_block(tree_data)
            html_tree += "\n"
            
            processed_lines.append(html_tree)
        else:
            processed_lines.append(line)


    full_markdown_content = "".join(processed_lines)

    ## Translate the rest of the file into html

    #html_body_content = mistletoe.markdown(full_markdown_content)
    full_markdown_content = checklistMD_from_string(full_markdown_content)

    full_markdown_content = CenterText(full_markdown_content,"center.md")


    html_body_content = mistletoe.markdown(full_markdown_content)
    

    # Add the needed headers
    final_document = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <link href="style.css" rel="stylesheet"/>
    </head>
    <body>
        {html_body_content}
    </body>
    </html>

    """


    with open("T.md", "w", encoding="utf-8") as fout:
        fout.write(full_markdown_content)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
        fout.write(final_document)

    print("Le fichier output.html a été généré avec succès avec un seul appel Mistletoe !")
