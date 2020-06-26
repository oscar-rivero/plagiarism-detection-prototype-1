#modulo comparador

from nltk import word_tokenize
from funciones import elmayor, stopen

from nltk.corpus import wordnet

from modulo_lematizador import lematizar,preparar
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
    
        lemas_texto=lematizar(tags_texto)
        
        coinc_url=[lema for lema in preparar(plagio) if lema in lemas_texto and lema.lower() not in stopen and lema.isalpha()]
    
        paras=textr.split(' \n  \n ')
        
        token_paras=[word_tokenize(para) for para in paras]
        
        token_paras=[[token.lower() for token in para if token.isalpha()] for para in token_paras]
        
        etiq_paras=[tagger.tag(para) for para in token_paras]
        
        lema_paras=[lematizar(para) for para in etiq_paras]
        
        sets_paras=[set(para) for para in lema_paras]
        
        set_coinc_url=set(coinc_url)
        
        set_plag = set(preparar(plagio))
        
        qs=[]
        for i,set_orig in enumerate(sets_paras):
            
            # if len(set_orig)>len(set_plag)*4:
            #     continue
            # elif len(set_orig)<len(set_plag)/4:
            #     continue
            
            # else:
                
            q=set_coinc_url.intersection(set_orig)

            lem_dif_orig=set_orig-set_plag 
            
            lem_dif_plag=set_plag-set_orig
            

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
            
            
            sinonimos=[]
            
            for entrada_plg in sinonimos_plagio:
                for entrada_original in sinonimos_orig:
                    if entrada_plg[0]!=entrada_original[0]:
                        for sinonimo in entrada_original[1]:
                            haysin=False
                            seguridad=0
                            if sinonimo in entrada_plg[1]:
                                haysin=True
                                seguridad+=1
                        if haysin==True:
                            sinonimos.append((entrada_plg[0], entrada_original[0]))
            
            qs.append((len(q)+len(sinonimos),i, len(q), sinonimos))
            grtr=elmayor([q for q,i,l,s in qs])
        
        
        i=[i for q,i,l,s in qs if q==grtr][0]
    
        l=[l for q,i,l,s in qs if q==grtr][0]
        
        s=[s for q,i,l,s in qs if q==grtr][0]
        

        para=paras[i]
        
        return (url, para, grtr, len(lema_paras[i]), l, s, plagio)

def pprint(coinc):
    print("La url donde se ha encontrado el texto:", coinc[0])
    print()
    print("El párrafo sospechoso:", )
    print(coinc[-1])
    print()
    print("El párrafo que se ha encontrado:",)
    print(coinc[1])
    print()
    print("El número de palabras léxicas originales del párrafo que se ha encontrado:", coinc[3])
    print("El número de coincidencias lemáticas entre ambos textos:", coinc[4])
    print("El número de sinónimos:", len(coinc[5]))
    print("El número de similitudes léxicas entre coincidencias lemáticas y sinónimos:", coinc[2])
    print("Los sinónimos hallados:", coinc[5])
    