import argparse
import os
import re

def main(path):
    with open(path, "r") as f:
        contents = f.read()
        blocks = contents.split("\n-")
        cards = [card for card in blocks if '#' not in card]
        outfile = path[:-2] + "txt"
        with open(outfile, "w") as f:
            for card in cards:
                if "    - " in card:
                    card = '<br>'.join([line for line in card.split('\n') if "    - " in line])
                    i=1
                    while re.search("{{(?!c)", card):
                        card = re.sub("{{(?!c)", "{{c"+str(i)+"::", card, count=1)
                        i += 1
                    card = card.replace("    ", '')
                    f.write(card+'\n')
                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    assert os.path.isfile(args.path)
    main(args.path)