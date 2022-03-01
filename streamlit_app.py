import nltk
import streamlit as sl
from modulo_cargar_tagger import tagger

sl.write("# Prototipo de sistema de detección de plagio")
sl.write("Hola, esto es una demostración en español de lo que hace mi Trabajo de Final de Grado")

txt = sl.text_area("Introduce el texto que deseas buscar")

if txt:
    sl.write("Ahora vamos a etiquetar estas palabras con mi etiquetador.")

    tokens_texto=nltk.word_tokenize(txt)

    tags_texto=tagger.tag(tokens_texto)

    sl.write("El output:")
    sl.write(tags_texto)
    


