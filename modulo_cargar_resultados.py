#modulo cargar_resultados
"""
modulo que carga el etiquetador gramatical generado previamente con tagger_init.py
"""
from pickle import load as pklLoad
carga = open('results.pkl', 'rb')
resultados = pklLoad(carga)

