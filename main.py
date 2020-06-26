#main
"""
Archivo principal del prototipo.
Carga todos los módulos necesarios para el funcionamiento del programa
y ejecuta un código para dar un ejemplo de detección de plagio.
"""
from funciones import elmayor
from modulo_textos import txtsstr
from modulo_comparador import buscar_para, pprint

cargar=-1

while cargar not in ('s', 'n'):
    cargar=input("Cargar resultados guardados? s/n")
if cargar=='s':
    from modulo_cargar_resultados import resultados
elif cargar=='n':
    from modulo_buscador import masfreq as resultados

print("Procesando resultados...")
total=[]
for i,text in enumerate(resultados):
    para_coinc=[]
    for url in text:
        print("Comparando texto", i+1, "con", url)
        coinc=buscar_para(txtsstr[i], url)
        para_coinc.append(coinc)
        
    total.append(para_coinc)

print()

#final=[]
for i,para_coinc in enumerate(total):
    print("Texto", i+1,":")
    print("__________________________________________")
    print()
    if para_coinc!=None:
        for coinc in para_coinc:
            if coinc!=None:
                if elmayor([coinc[2] for coinc in para_coinc if coinc!=None])==coinc[2]:
                    pprint(coinc)
                    print()
                    #final.append((txtsstr[i],coinc[1],coinc[0],coinc[2]), coinc[3])