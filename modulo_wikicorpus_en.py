#modulo wikicorpus_en
"""
crear una subclase de CorpusReader de nltk que lea el corpus wikicorpus
"""

from os import listdir
from nltk.corpus import PlaintextCorpusReader
import nltk
import nltk.data
from nltk.tokenize import *

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *

class WikiCorpusReader(CorpusReader):
    """
    Reader for corpora that consist of plaintext documents.  Paragraphs
    are assumed to be split using blank lines.  Sentences and words can
    be tokenized using the default tokenizers, or by custom tokenizers
    specificed as parameters to the constructor.

    This corpus reader can be customized (e.g., to skip preface
    sections of specific document formats) by creating a subclass and
    overriding the ``CorpusView`` class variable.
    """

    CorpusView = StreamBackedCorpusView
    """The corpus view class used by this reader.  Subclasses of
       ``PlaintextCorpusReader`` may specify alternative corpus view
       classes (e.g., to skip the preface sections of documents.)"""

    def __init__(
        self,
        root,
        fileids,
        word_tokenizer=WordPunctTokenizer(),
        sent_tokenizer=nltk.data.LazyLoader('tokenizers/punkt/english.pickle'),
        para_block_reader=read_blankline_block,
        encoding='utf8',
    ):
        """
        Construct a new plaintext corpus reader for a set of documents
        located at the given root directory.  Example usage:

            >>> root = '/usr/local/share/nltk_data/corpora/webtext/'
            >>> reader = PlaintextCorpusReader(root, '.*\.txt') # doctest: +SKIP

        :param root: The root directory for this corpus.
        :param fileids: A list or regexp specifying the fileids in this corpus.
        :param word_tokenizer: Tokenizer for breaking sentences or
            paragraphs into words.
        :param sent_tokenizer: Tokenizer for breaking paragraphs
            into words.
        :param para_block_reader: The block reader used to divide the
            corpus into paragraph blocks.
        """
        CorpusReader.__init__(self, root, fileids, encoding)
        self._word_tokenizer = word_tokenizer
        self._sent_tokenizer = sent_tokenizer
        self._para_block_reader = para_block_reader

    def raw(self, fileids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, string_types):
            fileids = [fileids]
        raw_texts = []
        for f in fileids:
            _fin = self.open(f)
            raw_texts.append(_fin.read())
            _fin.close()
        return concat(raw_texts)

    def words(self, fileids=None):
        """
        :return: the given file(s) as a list of words
            and punctuation symbols.
        :rtype: list(str)
        """
        return concat(
            [
                self.CorpusView(path, self._read_word_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )

    def sents(self, fileids=None):
        """
        :return: the given file(s) as a list of
            sentences or utterances, each encoded as a list of word
            strings.
        :rtype: list(list(str))
        """
        if self._sent_tokenizer is None:
            raise ValueError('No sentence tokenizer for this corpus')

        return concat(
            [
                self.CorpusView(path, self._read_sent_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )
    
    def tags(self, fileids=None):
        """
        :return: the given file(s) as a list of words
            and punctuation symbols.
        :rtype: list(str)
        """
        return concat(
            [
                self.CorpusView(path, self._read_tag_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )
    
    def lemmas(self, fileids=None):
        """
        :return: the given file(s) as a list of words
            and punctuation symbols.
        :rtype: list(str)
        """
        return concat(
            [
                self.CorpusView(path, self._read_lemma_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )
    
    def tagged_sents(self, fileids=None):
        """
        :return: the given file(s) as a list of
            sentences or utterances, each encoded as a list of word
            strings.
        :rtype: list(list(str))
        """
        if self._sent_tokenizer is None:
            raise ValueError('No sentence tokenizer for this corpus')

        return concat(
            [
                self.CorpusView(path, self._read_tag_sent_block, encoding=enc)
                for (path, enc, fileid) in self.abspaths(fileids, True, True)
            ]
        )



    # def paras(self, fileids=None):
    #     """
    #     :return: the given file(s) as a list of
    #         paragraphs, each encoded as a list of sentences, which are
    #         in turn encoded as lists of word strings.
    #     :rtype: list(list(list(str)))
    #     """
    #     if self._sent_tokenizer is None:
    #         raise ValueError('No sentence tokenizer for this corpus')

    #     return concat(
    #         [
    #             self.CorpusView(path, self._read_para_block, encoding=enc)
    #             for (path, enc, fileid) in self.abspaths(fileids, True, True)
    #         ]
    #     )

    def _read_word_block(self, stream):
        words = []
        for i in range(1600):  # Read 20 lines at a time.
            line=self._word_tokenizer.tokenize(stream.readline())
            
            if len(line)>1 and line[0] =='<' and line[1]=='doc'and line[-1]=='">':
                continue
            elif len(line)>0 and line[0]=='</':
                continue
            elif len(line)>0 and line[0]=="ENDOFARTICLE":
                continue
            elif len(line)>3:
                words.append(line[0])
        return words

    def _read_sent_block(self, stream):
        reraw = " ".join(self._read_word_block(stream))
        
        sents = []
        
        sents.extend(
            [
                self._word_tokenizer.tokenize(sent)
                for sent in self._sent_tokenizer.tokenize(reraw)
            ]
        )
        
        return sents

    def _read_tag_block(self, stream):
        tags = []
        for i in range(1600):  # Read 20 lines at a time.
            line=self._word_tokenizer.tokenize(stream.readline())
            
            if len(line)>1 and line[0] =='<' and line[1]=='doc'and line[-1]=='">':
                continue
            elif len(line)>0 and line[0]=='</':
                continue
            elif len(line)>0 and line[0]=="ENDOFARTICLE":
                continue
            elif len(line)>3:
                tags.append((line[0],line[2].lower()))
        return tags
    
    def _read_lemma_block(self, stream):
        lemmas = []
        for i in range(1600):  # Read 20 lines at a time.
            line=self._word_tokenizer.tokenize(stream.readline())
            
            if len(line)>1 and line[0] =='<' and line[1]=='doc'and line[-1]=='">':
                continue
            elif len(line)>0 and line[0]=='</':
                continue
            elif len(line)>0 and line[0]=="ENDOFARTICLE":
                continue
            elif len(line)>3:
                tags.append((line[0],line[1].lower()))
        return lemmas



    def _read_tag_sent_block(self, stream):
        entradas = [[token,tag] for (token, tag) in self._read_tag_block(stream)]
        reraw = " ".join([token for (token, _) in entradas])
        
        tags = [tag for (_, tag) in entradas]
        tagged_sents = []
        
        i=0
        for sent in self._sent_tokenizer.tokenize(reraw):
            tagged_sent = []
            for token in self._word_tokenizer.tokenize(sent):
                tupla = []
                tupla.append(token)
                tupla.append(tags[i])
                i+=1
                tagged_sent.append(tuple(tupla))
            tagged_sents.append(tagged_sent)
        
        return tagged_sents
    
    
    # def _read_para_block(self, stream):
    #     reraw = " ".join(self._read_word_block_reraw(stream))
        
    #     paras = []
    #     for para in self._para_block_reader(stream):
    #         paras.append(
    #             [
    #                 self._word_tokenizer.tokenize(sent)
    #                 for sent in self._sent_tokenizer.tokenize(para)
    #             ]
    #         )
    #     return paras

wikicorpus = WikiCorpusReader('C:\\corpus\\wikicorpus_en', listdir('C:\\corpus\\wikicorpus_en'), word_tokenizer=WordPunctTokenizer(), sent_tokenizer=nltk.data.LazyLoader('tokenizers/punkt/english.pickle'), para_block_reader=read_blankline_block, encoding='latin-1')
