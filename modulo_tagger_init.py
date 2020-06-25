"""
etiquetador wikicorpus english
"""

def universal_tags(tg_sts):
    u_tgs=[]
    for sent in tg_sts:
        s=[]
        for (w,t) in sent:
            tpl=[]
            tpl.append(w)
            
            if t.lower().startswith('z'):  
                tpl.append('NUM')
            elif t.lower()=='w':
                tpl.append('X')
            elif t.lower().startswith('i'):
                tpl.append('INTJ')
            elif t.lower().startswith('j'):
                tpl.append('ADJ')
            elif t.lower().startswith('r') or t.lower()=='wrb':
                tpl.append('ADV')
            elif t.lower()=='cc':
                tpl.append('CCONJ')
            elif t.lower()=='dt' or t.lower()=='wdt' or t.lower()=='pdt':
                tpl.append('DET')
            elif t.lower()=='uh':
                tpl.append('INTJ')
            elif t.lower().startswith('n'):
                tpl.append('NOUN')                
            elif t.lower()=='rp':
                tpl.append('PART')
            elif t.lower()=='to':
                tpl.append('PART')
            elif t.lower()=='ex': 
                tpl.append('PRON')                
            elif t.lower()=='wp':
                tpl.append('PRON')
            elif t.lower()=='prp':
                tpl.append('PRON')
            elif t.lower()=='prp$':
                tpl.append('PRON')
            elif t.lower()=='wp$':
                tpl.append('PRON')
            elif t.lower().startswith('f'):
                tpl.append('PUNCT')                
            elif t.lower().startswith('v'):
                tpl.append('VERB')                
            elif t.lower().startswith('md'):
                tpl.append('AUX')                
            else:
                tpl.append('X')
            s.append(tuple(tpl))
            
        u_tgs.append(s)
    return u_tgs

from modulo_wikicorpus_en import wikicorpus
inicio = 14500
long = 50000

train = int(long*0.9)
test = int(long*0.1)

print("wiki train")
wiki_train = universal_tags(wikicorpus.tagged_sents()[inicio:inicio+train])
print("wiki test")
wiki_test = universal_tags(wikicorpus.tagged_sents()[inicio+train:inicio+train+test])

from nltk import DefaultTagger

default_tagger = DefaultTagger('NOUN')

#entrenamos el affixtagger
from nltk import AffixTagger

print("affix tagger")
affix_tagger = AffixTagger(wiki_train, backoff=default_tagger)


#inicializamos el brillTagger
from nltk import BrillTaggerTrainer
from nltk.tag.brill import Template
from nltk.tag.brill import Word, Pos


templates = [ 
            Template(Pos([-1])), 
            Template(Pos([1])), 
            Template(Pos([-2])), 
            Template(Pos([2])), 
            Template(Pos([-2, -1])), 
            Template(Pos([1, 2])), 
            Template(Pos([-3, -2, -1])), 
            Template(Pos([1, 2, 3])), 
            Template(Pos([-1]), Pos([1])), 
            Template(Word([-1])), 
            Template(Word([1])), 
            Template(Word([-2])), 
            Template(Word([2])), 
            Template(Word([-2, -1])), 
            Template(Word([1, 2])), 
            Template(Word([-3, -2, -1])), 
            Template(Word([1, 2, 3])), 
            Template(Word([-1]),Word([1])), 
            ] 

#entrenamos el unigramtagger
from nltk import UnigramTagger
from nltk import BigramTagger
from nltk import TrigramTagger

print("unigram tagger")
unigram_tagger = UnigramTagger(wiki_train, backoff=affix_tagger)

print("bigram  tagger")
bigram_tagger = BigramTagger(wiki_train, backoff=unigram_tagger)

print("trigram tagger")
trigram_tagger= TrigramTagger(wiki_train, backoff=bigram_tagger)

#creamos el trainer del brilltagger
trainer = BrillTaggerTrainer(trigram_tagger, templates)

#entrenamos el brill_tagger
wiki_tagger = trainer.train(wiki_train, max_rules=200)

#guardamos el brill_tagger en un archivo
from pickle import dump
output = open('wiki_tagger_u.pkl', 'wb')
dump(wiki_tagger, output,-1)
output.close()

#el brill tagger sobre el test corpus
wiki_eval = wiki_tagger.evaluate(wiki_test)

print(wiki_eval)