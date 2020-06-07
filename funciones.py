"""funciones
"""

def elmayor(numeros):
    for i,numero in enumerate(numeros):
        if i==0:
            elmayor=numero
        if i>0:
            if elmayor<numeros[i]:
                elmayor=numeros[i]
    return elmayor

from nltk.corpus import stopwords

def stopen():
    stopen=stopwords.words('english')
    return stopen
