# -*- coding: utf-8 -*-
"""
modulo que carga el modelo fasttext desde una archivo pkl generado previamente por el modulo fasttext_init.py
"""

from pickle import load as pklLoad
carga = open('fasttext_wikicorpus_sents[14500+50mil].pkl', 'rb')
modelo = pklLoad(carga)