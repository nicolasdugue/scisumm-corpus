#from nltk import import 
from nltk.classify.rte_classify import lemmatize
class NLPProcessor:
    """
        Responsible of all the natural language processing tasks, such as
        stemming, lemmatisation, removing stop words ..  
    """
    @staticmethod
    def processText( text):
        text = NLPProcessor.removeStopWords(text)
        text = NLPProcessor.lemmatizeText(text)
        return text
    
    @staticmethod
    def lemmatizeText(text):
        return text
    
    @staticmethod
    def stemmetizeText(text):
        return text
    
    @staticmethod
    def removeStopWords(text):
        return text
    
