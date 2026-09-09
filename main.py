import mistletoe
import re
from pathlib import Path
from textwrap import dedent
SHORTCUT = "!!"
FILE = "testmark.md"

def build_tree(path : str, max_depth, current_depth=1) -> dict | list:
    """
    Reads a folder and builds a tree consisting of all the files at a certain depth.
    Can be used with Build_html

    It returns a dict or list depending on the depth
    """

    if path in [r'\\',r'\\'[0]]:
        path = r''
    path = Path(path)
    
    if path.is_file(): ## Make sure the path is not just a file
        return path.name
        
    if current_depth == max_depth: #Make sure not to go infinetly
        
        return [f.name for f in path.iterdir() if not f.name.startswith('.')]
        
    tree = {}
    for item in path.iterdir():

        if item.name.startswith('.'): #ignore folders with . before their name
            continue
            
        if item.is_dir(): # if the item is a folder go into it to continue the tree
            tree[item.name] = build_tree(item, max_depth, current_depth + 1)
        else:
            tree[item.name] = item.name
            
    return tree

def build_html(tree: dict | list | str) -> str:
    """
    Builds the html tree
    """
    html = ''
    
    # 1. if a list
    if isinstance(tree, list):
        for item in tree:
            
            html += f'<li><span class="file">{item}</span></li>' 

            
    # 2. if string
    elif isinstance(tree, str):
        html += f'<li><span class="file">{tree}</span></li>' 

    # 3. if dict 
    elif isinstance(tree, dict):
        for folder_name, content in tree.items():
            if isinstance(content,list):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content)
                html += '</ul></li>'
            if isinstance(content,str):
                html += f'<li><span class="file">{content}</span></li>' 
            if isinstance(content,dict):
                html += f'<li><span class="folder">{folder_name}</span><ul>'
                html += build_html(content)
                html += '</ul></li>'
    return html

def render_page(tree_dict):

    corps_arbre = build_html(tree_dict) 
    
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


OUTPUT_FILE = "output.html"
with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
    fout.write(final_html)
print("Le head a été ajouté avec succès dans 'index.html' !")


