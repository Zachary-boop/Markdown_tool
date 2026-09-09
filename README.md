# Markdown_tool

## Project Overview
Post-processeur commonmark ajoutant la fonctionallite de créer un arbre complet du folder avec seulement son path.
## Project setup
This project is based on the mistletoe library. 

## Team
* Product owner : Philippe Gauthier
* Scrum Master : Amélie Sarrazin
* Équipe développeur  : Zachary Roy

## Guide d'utilisation
Le fichier markdown d'entré doit être modifié à la ligne 80 du code

Le code a besoin d'une ligne qui commance avec !!
```
!! C:\Users\user1\Desktop 2
```
La commande a deux paramètres
* le path (absolu ou relatif au code)
* La depth de recherche

Si le code n'a pas les permission pour accéder à un folder, il ne va rien affiché

## Dépendences
Le projet à besoin des libraries 
* mistletoe
* bs4

Pour les installé, un script .bat à été fait
```bash
cd Path/to/folder/scripts
setup_python.bat
```
Sinon il peut être exécuté avec double click dans l'explorateur de fichier.

Il est aussi possible d'installé à la main la list de dépendance dans le fichier requirement.txt
