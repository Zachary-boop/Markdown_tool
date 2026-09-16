import mistletoe
import re
from pathlib import Path
<<<<<<< Updated upstream
from textwrap import dedent
=======

>>>>>>> Stashed changes
SHORTCUT = "!!"
FILE = "testmark.md"
OUTPUT_FILE = "output.html"

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
    
<<<<<<< Updated upstream
    raw_html =f"""<!DOCTYPE html>
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
    return raw_html

with open(FILE ,"r") as fin:
    CommonMark_content = fin.readlines()

indexs = []
for index, line in enumerate(CommonMark_content):
    if line[0:2] == "!!":
        print(line)
        indexs.append(index)

print(indexs)

final_html = ""
last_index = 0
for index in indexs: # Add everything to the html until the last command
    
    parameters = CommonMark_content[index][1 + len(SHORTCUT):]
    path, depth = parameters.strip().split(' ')
    
    
    tree = build_tree(path, depth)
    
    
    markdown_chunk = "\n".join(CommonMark_content[last_index:index])
    final_html += mistletoe.markdown(markdown_chunk)
    final_html += render_page(tree)
    
    
    last_index = index + 1 

if indexs: # Add the remaining chunk of text to the html
    remaining_chunk = "\n".join(CommonMark_content[last_index:])
    final_html += mistletoe.markdown(remaining_chunk)

else: ## If no command
    final_html += mistletoe.markdown("\n".join(CommonMark_content))
=======
    return f'<div class="file-tree"><ul>{corps_arbre}</ul></div>'


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
>>>>>>> Stashed changes


with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
    fout.write(final_document)

print("Le fichier output.html a été généré avec succès avec un seul appel Mistletoe !")