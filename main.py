import mistletoe
from bs4 import BeautifulSoup
import re
from Code.file import build_tree
from pathlib import Path

SHORTCUT = "!!"
def build_tree(path, max_depth, current_depth=1):
    if path in [r'\\',r'\\'[0]]:
        path = r''
    path = Path(path)
    
    if path.is_file():
        return path.name
        
    if current_depth == max_depth:
        # On filtre les éléments cachés à la profondeur maximale
        return [f.name for f in path.iterdir() if not f.name.startswith('.')]
        
    tree = {}
    for item in path.iterdir():
        # ICI : On ignore complètement si le nom commence par un point
        if item.name.startswith('.'):
            continue
            
        if item.is_dir():
            tree[item.name] = build_tree(item, max_depth, current_depth + 1)
        else:
            tree[item.name] = item.name
            
    return tree


def build_html(tree: dict | list | str) -> str:
    html = ''
    
    # 1. Cas d'une liste
    if isinstance(tree, list):
        for item in tree:
            # On rappelle la fonction pour gérer si l'item est un dictionnaire, sous-liste ou str
            html += f'<li><span class="file">{item}</span></li>' 

            
    # 2. Cas d'une chaîne
    elif isinstance(tree, str):
        html += f'<li><span class="file">{tree}</span></li>' 

    # 3. Cas d'un dictionnaire 
    elif isinstance(tree, dict):
        for folder_name, content in tree.items():
            if isinstance(content,list):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content) # On passe le contenu (liste, dict, etc.)
                html += '</ul></li>'
            if isinstance(content,str):
                html += f'<li><span class="file">{content}</span></li>' 
            if isinstance(content,dict):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content) # On passe le contenu (liste, dict, etc.)
                html += '</ul></li>'
    return html

def render_page(tree_dict):
    # Appel de la fonction récursive corrigée au message précédent
    corps_arbre = build_html(tree_dict) 
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <link href="style.css" rel="stylesheet"/>
</head>
<body>
    <div class="file-tree">
        <ul>
            {corps_arbre}
        
    </div>
</body>
</html>"""

with open('testmark.md', 'r') as fin:
    html_content = mistletoe.markdown(fin)
# 2. Analyser le code avec BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# 3. Créer la balise <head> principale
head_tag = soup.new_tag("head")

# 4. Créer les balises enfants à mettre dans le head
meta_charset = soup.new_tag("meta", charset="UTF-8")

title_tag = soup.new_tag("title")
title_tag.string = "Static HTML/CSS File Tree"

link_css = soup.new_tag("link", rel="stylesheet", href="style.css")

# 5. Assembler le <head> en y ajoutant les balises créées
head_tag.append(meta_charset)

head_tag.append(title_tag)
head_tag.append(link_css)

# 6. Insérer le <head> tout au début du document (ou au début de la balise <html>)
if soup.html:
    soup.html.insert(0, head_tag)
else:
    # Si la balise <html> n'existe pas du tout, on l'ajoute au début du fichier
    soup.insert(0, head_tag)


while True:
    element = soup.find(string=re.compile(SHORTCUT))
    if element is None:
        break
    parameters = element[1+len(SHORTCUT):]
    path,depth = parameters.split(' ')
    print(path,depth)
    try:
        print(f'\npath : {path}')
        print(f'depth : {depth}\n')
        try : 
            depth = int(depth)
        except:
            depth = 1
        tree = build_tree(path,depth)
        print(tree)
        html = render_page(tree)
        
    except:
        html = ''
        pass
    nouveau_html = BeautifulSoup(html, "html.parser")
    
    balise_parente = element.parent
    balise_parente.clear()
    balise_parente.append(nouveau_html)

#add stuff
with open("output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("Le head a été ajouté avec succès dans 'index.html' !")
