#modulo comparador

from nltk import word_tokenize
from funciones import elmayor, stopen

from nltk.corpus import wordnet

from modulo_lematizador import lematexto,lemas_plagio
from modulo_cargar_tagger import tagger

import urllib
import html2text

stopen=stopen()

def buscar_para(plagio, url):
    
    file=None
    try:
        file = urllib.request.urlopen(url)
    except:
        pass
    if file!=None:
        try:
            doc = file.read().decode('utf- 8')
        except:
            doc = file.read().decode('latin-1')
                
    
        h = html2text.HTML2Text()
        h.ignore_links = True
        
        text = h.handle(doc)
    
        textr=text.replace('\n', ' \n ')
        textr=textr.replace('*', '')
        textr=textr.replace('\\', '')
    
        tokens_texto=word_tokenize(textr)
        
        tokens_texto=[token.lower() for token in tokens_texto]
        
        tags_texto=tagger.tag(tokens_texto)
    
        lemas_texto=lematexto(tags_texto)
        
        coinc=[lema for lema in lemas_plagio(plagio) if lema in lemas_texto and lema.lower() not in stopen and lema.isalpha()]
    
        paras=textr.split(' \n  \n ')
        
        token_paras=[word_tokenize(para) for para in paras]
        
        token_paras=[[token.lower() for token in para if token.isalpha()] for para in token_paras]
        
        etiq_paras=[tagger.tag(para) for para in token_paras]
        
        lema_paras=[lematexto(para) for para in etiq_paras]
        
        sets_paras=[set(para) for para in lema_paras]
        
        set_coinc=set(coinc)
        
        qs=[]
        for i,sett in enumerate(sets_paras):
            q=set_coinc.intersection(sett)
            

            set_plag = set(lemas_plagio(plagio))

            lem_dif_orig=sett-set_plag 
            
            lem_dif_plag=set_plag-sett
            

            #aqui compruebo los sinónimos entre los dos textos
            sinonimos_plagio=[]
            for nombre in lem_dif_plag:
                sinonimos=[]
                for syn in wordnet.synsets(nombre):
                    for lema in syn.lemmas():
                        sinonimos.append(lema.name())
                sinonimos_plagio.append((nombre,sinonimos))
            
            sinonimos_plagio = [entrada for entrada in sinonimos_plagio if len(entrada[1])>0]
            
            sinonimos_orig=[]
            for nombre in lem_dif_orig:
                sinonimos=[]
                for syn in wordnet.synsets(nombre):
                    for lema in syn.lemmas():
                        sinonimos.append(lema.name())
                sinonimos_orig.append((nombre,sinonimos))
            
            sinonimos_orig = [entrada for entrada in sinonimos_orig if len(entrada[1])>0]
            
            for plg in sinonimos_plagio:
                for original in sinonimos_orig:
                    if plg[0]!=original[0]:
                        for entrada in original[1]:
                            haysin=False
                            seguridad=0
                            if entrada in plg[1]:
                                haysin=True
                                seguridad+=1
                        if haysin==True:
                            q.add((plg[0], original[0]))
            
            qs.append((len(q),i))
            grtr=elmayor([q for q,i in qs])
        
        
        i=[i for q,i in qs if q==grtr][0]
    
        para=paras[i]
        
        return (url, para, grtr)
