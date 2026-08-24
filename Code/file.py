from pathlib import Path
import pprint

def build_tree(path, max_depth, current_depth=1):
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

if __name__ == "__main__":
    mypath = Path(r'C:\Users\royza\Desktop\Labo\Prog4\Markdown_tool')
    profond_max = 2

    dossier_arbre = build_tree(mypath, max_depth=profond_max)
    pprint.pprint(dossier_arbre)
