#modulo lematizador
from nltk.stem import WordNetLemmatizer
from modulo_cargar_tagger import tagger
from nltk import word_tokenize


lemmatizer=WordNetLemmatizer()

def lematizar(texto):
    
    texto_pl_lemas=[]
    for (w,t) in texto:
        if t=='NOUN':
            r='n'
        elif t=='VERB':
            r='v'
        elif t=='ADJ':
            r='a'
        elif t=='ADV':
            r='r'
        else:
            r=None
    
        if r!=None:
            texto_pl_lemas.append(lemmatizer.lemmatize(w, pos=r))
        else:
            texto_pl_lemas.append(w)
    return texto_pl_lemas



def preparar(texto):
    tokens_texto=word_tokenize(texto)
    
    tags_texto=tagger.tag(tokens_texto)
    
    return lematizar(tags_texto)

