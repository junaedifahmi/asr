import logging
import os.path
import sys
 
from gensim.corpora import WikiCorpus
 
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
 
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))
 
namaFileInput = sys.argv[1]
namaFileOutput = sys.argv[2]
 
space = " "
i = 0
 
output = open(namaFileOutput, 'w')
 
# lower=False: huruf kecil dan besar dibedakan
wiki = WikiCorpus(namaFileInput, lemmatize=False, dictionary={}, lower=True)
# wiki.save_corpus(namaFileOutput)
for text in wiki.get_texts():
    output.write(' '.join(text) + '\n')
    print(' '.join(text))
    i = i + 1
    if i % 10000 == 0:
        logger.info("Saved " + str(i) + " articles")
 
output.close()
logger.info("Finished Saved " + str(i) + " articles")
