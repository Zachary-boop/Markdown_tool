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

