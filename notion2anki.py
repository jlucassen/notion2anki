import argparse
import os
import zipfile
import re

def split_by_header(contents, level):
    split = '\n' + '#' * level + ' '
    groups = contents.split(split)
    out = {}
    for group in groups:
        if len(group) == 0: continue
        tag = group.split("\n")[0]
        body = '\n'+'\n'.join(group.split("\n")[1:])
        out[tag] = body
    return out

def number_clozes(card):
    i=1
    while re.search("{{(?!(c\d))", card):
        card = re.sub("{{(?!(c\d))", "{{c"+str(i)+"::", card, count=1)
        i += 1
    return card

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
        contents = '\n'.join(contents.split("\n")[1:]) # remove title line
        groups_1 = split_by_header(contents, 1)
        with open(path[:-3]+'.txt', 'w') as f:
            for tag1, group1 in groups_1.items():
                groups_2 = split_by_header(group1, 2)
                for tag2, group2 in groups_2.items():
                    groups_3 = split_by_header(group2, 3)
                    for tag3, group3 in groups_3.items():
                        tag = tag1 + ((':'+tag2) if len(tag2) > 0 else '') + ((':'+tag3) if len(tag3) > 0 else '')
                        cards = group3.split("\n- ")
                        for card in cards:
                            card = card.strip()
                            if len(card) == 0: continue # empty card
                            card.replace('\n', '<br>')
                            card = number_clozes(card)
                            card = card + f"|{tag}"
                            f.write(card+'\n')      









            # tag_groups = contents.split("### ")
            # for tag_group in tag_groups:
            #     if not tag_group.startswith('- '): # no bullet at start, must be a tag
            #         tag = tag_group.split("\n- ")[0]
            #         bullets = tag_group.split('\n- ')[1:] # remove tag from bullets
            #     else:
            #         bullets = tag_group.split('\n- ')
            #     for bullet in bullets:
            #         if "    - " in bullet: # two deep detected, remove outer bullets and remove excess spaces from inner bullets
            #             card = '<br>'.join([line for line in bullet.split('\n') if "    - " in line])
            #             card = card.replace("    ", '')
            #         else: # just one deep, remove bullets
            #             card = bullet.replace('  - ', '')
            #         if card.endswith("\n"): card = card[:-1] # remove ending \n
            #         card = number_clozes(card)
            #         if tag is not None:
            #             card = card + f"|{title.lower().replace(' ','')}:{tag.lower().replace(' ', '')}"
            #         f.write(card+'\n')                  

                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    args = parser.parse_args()
    main(args.path)