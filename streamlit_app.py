import nltk
import streamlit as sl
from modulo_cargar_tagger import tagger

nltk.download('punkt')

sl.write("# My Tagger")
sl.write("Hello, this is a demonstration of text tagging with my own tagger.")

txt = sl.text_area("Introduce the text you want to POS tag.")

sl.write("You can use the following text, from the Featured Article of Wikipedia in English from 1 february 2022:")
sl.write("Hector Waller (4 April 1900 - 1 March 1942) was a senior officer in the Royal Australian Navy. Born in Benalla, Victoria, Waller entered the Royal Australian Naval College in 1913 and served in the First World War. He gained his first command in 1937, as captain of the destroyer HMS Brazen. In September 1939, he took command of HMAS Stuart and four other obsolete destroyers that together became known as the \"Scrap Iron Flotilla\". Waller was awarded the Distinguished Service Order and Bar, and twice mentioned in despatches, for his achievements in the Mediterranean. He then transferred to the South West Pacific as captain of the light cruiser HMAS Perth, and went down with his ship against heavy odds during the Battle of Sunda Strait in early 1942. He received a third mention in despatches posthumously, and in 2011 came under formal consideration for the award of the Victoria Cross for his performance as Perth's captain. The submarine HMAS Waller is named in his honour.")


if txt:
    sl.write("Now we are going to tag the text:")

    tokens_texto=nltk.word_tokenize(txt)

    tags_texto=tagger.tag(tokens_texto)

    sl.write("The output:")
    sl.write(tags_texto)
    


