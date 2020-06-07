#main
"""
Archivo principal del prototipo.
Carga todos los módulos necesarios para el funcionamiento del programa
y ejecuta un código para dar un ejemplo de detección de plagio.
"""
from nltk import word_tokenize
from funciones import elmayor
from modulo_textos import txtsstr
from modulo_buscador import masfreq
from modulo_comparador import buscar_para
from modulo_modelo import modelo as ft
from modulo_similaridad import similaridad


total=[]
for i,text in enumerate(masfreq):
    para_coinc=[]
    for url in text:
        coinc=buscar_para(txtsstr[i], url)
        para_coinc.append(coinc)
        
    total.append(para_coinc)


final=[]
for i,para_coinc in enumerate(total):
    if para_coinc!=None:
        for coinc in para_coinc:
            print(i)
            if coinc!=None:
                if elmayor([coinc[2] for coinc in para_coinc if coinc!=None])==coinc[2]:
                    final.append((txtsstr[i],coinc[1],coinc[0],coinc[2], similaridad(word_tokenize(coinc[1]), word_tokenize(txtsstr[i]), ft)))