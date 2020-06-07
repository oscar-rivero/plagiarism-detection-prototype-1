#modulo buscador
"""
módulo que genera la lista de resultados del buscador a partir de las frases encontradas en los textos
"""


from googlesearch import search
from nltk import FreqDist
from modulo_textos import sents_plagios

total=[]

for text in sents_plagios:
    results=[]
    for sent in text:
        for i in search(sent,# The query you want to run
                        tld = 'com',  # The top level domain
                        lang = 'es',  # The language
                        num = 10,     # Number of results per page
                        start = 0,    # First result to retrieve
                        stop = 10,  # Last result to retrieve
                        pause = 2.0,  # Lapse between HTTP requests
                       ):
            results.append(i)
            print(i)
    total.append(results)

masfreq=[[w for (w,i) in FreqDist(results).most_common(3)] for results in total]

