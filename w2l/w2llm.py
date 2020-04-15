import argparse
import re
import subprocess

# Argument definition
parser = argparse.ArgumentParser(description="Language construction for wav2letter engine")
parser.add_argument("--textfiles",nargs='+', help="source text files")
parser.add_argument("--kenlm", help="kenlm root directory")
parser.add_argument("--order",default='4', help="Order of the lm")
parser.add_argument("--out", help="output directori", default="./lm")

args = parser.parse_args()

# Preprocessing def

def cleaner(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w\s]', '', sentence)   # remove punctuation 
    sentence = re.sub(r'\r?\n|\r', '', sentence) # remove new line
    sentence = re.sub(r'\d','',sentence)
    return sentence

def cacah(kata):
    x = [c for c in kata]
    for i in range(len(x)):
        try:
            y = x[i+1]

            if x[i] == 'n' and y == 'y':
                x[i] = 'ny'
                x[i+1] = '#'
            elif x[i] == 'n' and y == 'g':
                x[i] = 'ng'
                x[i+1] = '#'
            elif x[i] == 's' and y == 'y':
                x[i] = 'sy'
                x[i+1] = '#'
            elif x[i] == 'k' and y == 'h':
                x[i] = 'kh'
                x[i+1] = '#'
            elif x[i] == 't' and y == 'h':
                x[i] = 'th'
                x[i+1] = '#'
            elif x[i] not in list('abcdefghijklmnopqrstuvwxyz') and x[i] != '#':
                x[i] = '|'
        except:
            pass
    x = [c for c in x if c != '#']

    return x
    

out = args.out

# Get all text
files = args.textfiles
texts = []

for file in files:
    text = []
    with open(file, 'r') as f:
        # Cleaning text
        text.append(f.readlines())
        for x in text:
            x = cleaner(x)
            texts.append(x)

print(texts[0:6])

ftext = open(out+'/text', 'w')
for text in texts:
    ftext.writelines(text+' ')
ftext.close()

lexicons = set()
for text in texts:
    lexicons.update(text.split())

flexicon = open(out+'/lexicon', 'w+')

for lexicon in lexicons:
    flexicon.writelines(lexicon+"\t"+' '.join(cacah(lexicon))+" |\n")

# Building lm
kenlm = args.kenlm+'/build/bin/'
command = kenlm+'/lmpz'
command += ' -o ' + str(args.order)
command += ' --prune 0 10'
command += ' --discount_fallback=1 2 3 '
command += ' < '+out+'/text'
command += ' > '+out+'/lm.arpa'
command = command.split()

popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()

print("Arpa file was made at", out)

command = kenlm+'/build_binary' 
command += ' '+out+'/lm.arpa'
command += ' '+out+'/lm.bin'
command = command.split()
popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()
print("Binary was made at", out)