#modulo cargar_tagger
"""
modulo que carga el etiquetador gramatical generado previamente con tagger_init.py
"""
from pickle import load as pklLoad
carga = open('wiki_tagger_u.pkl', 'rb')
tagger = pklLoad(carga)

