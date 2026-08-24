import mistletoe
from bs4 import BeautifulSoup
import re
from Code.file import build_tree

SHORTCUT = "!!"


def build_html(tree : list) -> str:
    html = '''<body> <div class="file-tree"> <ul>'''
    for object in tree:
        if type(object) == list:
            print('file')
            html += f'<li><span class="file">{object}</span></li>'
        if type(object) == dict:
            print('dict')
    
    html += '<ul> </div> </body>'
    pass

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
    parameter = element[3:]
    print(parameter)
    try:
        tree = build_tree(parameter,2)
        print(tree)
        build_html(tree)
    except:
        html = ''
        pass
    nouveau_html = BeautifulSoup("e", "html.parser")
    
    balise_parente = element.parent
    balise_parente.clear()
    balise_parente.append(nouveau_html)

#add stuff
with open("output.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("Le head a été ajouté avec succès dans 'index.html' !")
