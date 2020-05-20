import argparse
import re
import subprocess
import os
import sys
from tqdm import tqdm

# Argument definition
parser = argparse.ArgumentParser(description="Language model construction for wav2letter engine")
parser.add_argument("--textfiles",nargs='+', help="source text files")
parser.add_argument("--kenlm", help="kenlm root directory")
parser.add_argument("--order",default='4', help="Order of the lm")
parser.add_argument("--out", help="output directori", default="./lm")

args = parser.parse_args()

if len(sys.argv) < 2 :
    parser.print_help()
    exit()

# Preprocessing def

def cleaner(sentence):
    sentence = sentence.encode("ascii", errors="ignore").decode() # Remove non ascii char
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w\s\_]', ' ', sentence)   # remove punctuation 
    sentence = re.sub(r'_+', '', sentence) # remove underscore
    sentence = re.sub(r'[aiueohm]{3,}', '', sentence)
    sentence = re.sub(r'\r?\n|\r', ' ', sentence) # remove new line
    sentence = re.sub(r'\d',' ',sentence) # remove any number
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
os.makedirs(out, exist_ok=True)
# Get all text
files = args.textfiles
texts = []


print("Reading files")
for file in tqdm(files):
    text = []
    with open(file, 'r') as f:
        # Cleaning text
        text.extend(f.readlines())
        for x in text:
            x = cleaner(x)
            texts.append(x)


print("Writing formated text")
ftext = open(out+'/text', 'w')
for text in tqdm(texts):
    ftext.writelines(text+' ')
ftext.close()

print("Getting lexicons")
lexicons = set()
for text in tqdm(texts):
    lexicons.update(text.split())

lexicons = sorted(lexicons)
flexicon = open(out+'/lexicon.txt', 'w+')

print("Writing lexicons")
for lexicon in tqdm(lexicons):
    flexicon.writelines(lexicon+"\t"+' '.join(cacah(lexicon))+" |\n")

# Building lm
kenlm = args.kenlm+'/build/bin/'
command = kenlm+'/lmplz'
command += ' -o ' + str(args.order)
command += ' --discount_fallback=0.5 1 1.5'
command += ' --prune 0 10'
command += ' --text '+out+'/text'
command += ' --arpa '+out+'/language_model_pruned.arpa'
print(command)
command = command.split()

popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()

print("Arpa file was made at", out)

command = kenlm+'/build_binary' 
command += ' -s'
command += ' '+out+'/language_model_pruned.arpa'
command += ' '+out+'/language_model_pruned.bin'
print(command)
command = command.split()
popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()
print("Binary was made at", out)

# Building lm
kenlm = args.kenlm+'/build/bin/'
command = kenlm+'/lmplz'
command += ' -o ' + str(args.order)
command += ' --discount_fallback=0.5 1 1.5'
command += ' --text '+out+'/text'
command += ' --arpa '+out+'/language_model.arpa'
print(command)
command = command.split()

popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()

print("Arpa file was made at", out)

command = kenlm+'/build_binary' 
command += ' -s'
command += ' '+out+'/language_model.arpa'
command += ' '+out+'/language_model.bin'
print(command)
command = command.split()
popen = subprocess.Popen(command, stdout=subprocess.PIPE)
popen.wait()
print("Binary was made at", out)