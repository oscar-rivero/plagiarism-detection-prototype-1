"""
modulo del modelo fasttext generado previamente con freetext_init.py
"""

from pickle import load as pklLoad
carga = open('fasttext_wikicorpus_sents[14500+50mil].pkl', 'rb')
modelo = pklLoad(carga)