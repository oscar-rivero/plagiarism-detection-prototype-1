#modulo similaridad

from funciones import stopen

from numpy import array

from scipy.spatial.distance import cosine

def vectores_vocab(vocab,modelo):
    vectores=[list(modelo.wv[palabra]) for palabra in vocab]
    return vectores

def centroide(vectores):
    vector_total=vectores[0]

    for vector in vectores[1:]:
        for i,valor in enumerate(vector_total):
            vector_total[i]=valor+vector[i]
            
    centroide=[valor_total/len(vectores) for valor_total in vector_total]
    return array(centroide)


def similaridad(lista1,lista2,modelo):    
    lista1=[palabra.lower() for palabra in lista1 if palabra not in stopen() and palabra.isalpha()]
    lista2=[palabra.lower() for palabra in lista2 if palabra not in stopen() and palabra.isalpha()]
  
    
    v_l1=vectores_vocab(lista1,modelo)
    v_l2=vectores_vocab(lista2,modelo)
    
    c_l1=centroide(v_l1)
    c_l2=centroide(v_l2)
    
    similaridad=1-cosine(c_l1,c_l2)
    return similaridad
