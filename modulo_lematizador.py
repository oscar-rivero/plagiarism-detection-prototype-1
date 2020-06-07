#modulo lematizador
from nltk.stem import WordNetLemmatizer
from modulo_cargar_tagger import tagger
from nltk import word_tokenize


lemmatizer=WordNetLemmatizer()

def lematexto(texto):
    
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



def lemas_plagio(plagio):
    tokens_plagio=word_tokenize(plagio)
    
    tags_plagio=tagger.tag(tokens_plagio)
    
    return lematexto(tags_plagio)

