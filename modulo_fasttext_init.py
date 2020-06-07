"""
generador de archivo pkl con el modelo semántico fast text sobre un segmento del corpus wikicorpus en inglés
"""


from wikicorpus_en import wikicorpus
from gensim.models.fasttext import FastText as fast

from time import time

from pickle import dump as guardar

inicio = 14500
long = 50000

train = int(long*0.9)
test = int(long*0.1)



print("Leyendo frases del wikicorpus sin procesar...")
wiki_train = wikicorpus.sents()[inicio:inicio+train]
print("Lectura finalizada.")
print("Iniciando preprocesado de frases.")

proc_wiki = []
for sent in wiki_train:
    sent2=[]
    for w in sent:
        if w.isalpha():
            w2=w.lower()
            sent2.append(w2)
    proc_wiki.append(sent2)
        
print("Preprocesado finalizado.")
print()
print("Iniciando modelado fasttext.")
print("Iniciando contador...")
t_ini = time()

modelo = fast(size=100)
modelo.build_vocab(proc_wiki)
modelo.train(sentences=proc_wiki, epochs=modelo.epochs, total_examples=modelo.corpus_count, total_words=modelo.corpus_total_words)

elapsed = time() - t_ini
print("Modelado finalizado.")
print("Tiempo de procesado: ")
print(elapsed)

archivo_modelo = open("fasttext_wikicorpus_sents[14500+50mil].pkl", "wb")
guardar(modelo, archivo_modelo)
archivo_modelo.close()
