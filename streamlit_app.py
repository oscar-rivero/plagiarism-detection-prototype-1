import nltk
import streamlit as sl
from modulo_cargar_tagger import tagger
import pandas as pd

nltk.download('punkt')

sl.write("# My Tagger")
sl.write("Hello, this is a demonstration of text tagging with my own tagger.")

txt = sl.text_area("Introduce the text you want to POS tag.")

sl.write("You can use the following text as an example (just copy-paste above):")
sl.write("The dog barks at the car.")


if txt:
    sl.write("Now we are going to tag the text:")

    tokens_texto=nltk.word_tokenize(txt)

    tags_texto=tagger.tag(tokens_texto)

    data = pd.DataFrame(tags_texto, columns=("Token", "POS Tag"))
    sl.write("The output:")
    sl.write(data)
    


