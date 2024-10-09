import argparse
import os
import zipfile
import re

def number_clozes(block):
    i=1
    while re.search("{{(?!(c\d))", block):
        block = re.sub("{{(?!(c\d))", "{{c"+str(i)+"::", block, count=1)
        i += 1
    return block

def main(path):
    if path is None:
        for file in os.listdir():
            if file.endswith('.zip'):
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall()
        paths = [p for p in os.listdir() if p[-3:]=='.md' and p != 'README.md']
    else:
        paths = [path]
    for path in paths:
        with open(path, "r") as f:
            contents = f.read()
        title = contents.split("\n")[0][2:]
        contents = '\n'.join([x for x in contents.split("\n")[1:] if len(x) > 0]) # remove deck title and empty lines
        outfile = path[:-2] + "txt"
        tag = None
        with open(outfile, "w") as f:
            tag_groups = contents.split("### ")
            for tag_group in tag_groups:
                if not tag_group.startswith('- '): # no bullet at start, must be a tag
                    tag = tag_group.split("\n- ")[0]
                    bullets = tag_group.split('\n- ')[1:] # remove tag from bullets
                else:
                    bullets = tag_group.split('\n- ')
                for bullet in bullets:
                    if "    - " in bullet: # two deep detected, remove outer bullets and remove excess spaces from inner bullets
                        card = '<br>'.join([line for line in bullet.split('\n') if "    - " in line])
                        card = card.replace("    ", '')
                    else: # just one deep, remove bullets
                        card = bullet.replace('  - ', '')
                    if card.endswith("\n"): card = card[:-1] # remove ending \n
                    card = number_clozes(card)
                    if tag is not None:
                        card = card + f"|{title.lower().replace(' ','')}:{tag.lower().replace(' ', '')}"
                    f.write(card+'\n')                  

                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    args = parser.parse_args()
    main(args.path)