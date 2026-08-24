import re
from bs4 import BeautifulSoup

html = "<p>!! 1</p>"
soup = BeautifulSoup(html, "html.parser")

# 1. On cherche le TEXTE qui contient "!!"
texte_cible = soup.find(string=re.compile("!!"))

if texte_cible:
    # 2. On remonte à la balise parente (le <p>)
    balise_parente = texte_cible.parent
    
    # 3. On remplace TOUT le contenu textuel de cette balise
    balise_parente.string = "Nouveau texte mis à jour"
else:
    print("Le texte avec '!!' n'a pas été trouvé.")

print(soup)
# Résultat attendu : <p>Nouveau texte mis à jour</p>
