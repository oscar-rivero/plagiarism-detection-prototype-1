import nltk
import streamlit as sl
from modulo_cargar_tagger import tagger

nltk.download('punkt')

sl.write("# My Tagger")
sl.write("Hello, this is a demonstration of the tagging of a text with my own tagger.")

txt = sl.text_area("Introduce the text you want to POS tag.")

if txt:
    sl.write("Now we are going to tag the text:")

    tokens_texto=nltk.word_tokenize(txt)

    tags_texto=tagger.tag(tokens_texto)

    sl.write("El output:")
    sl.write(tags_texto)
    


