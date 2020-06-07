#modulo cargar textos
from os import listdir
from nltk import sent_tokenize
dirlist=listdir('./plagios/')
txtsnames=[file for file in dirlist if file.endswith('.txt')]
txts=[open(str('./plagios/'+filename), 'r') for filename in txtsnames]
txtsstr=[file.read() for file in txts]
[file.close() for file in txts]
sents_plagios=[sent_tokenize(txt) for txt in txtsstr]