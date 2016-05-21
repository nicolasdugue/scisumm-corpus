import enchant
from nltk import word_tokenize


class Corrector:
    """
        :Note for resolving the import issue, you have to install the Lib, for more information:
         http://pythonhosted.org/pyenchant/tutorial.html#installing-the-package
         you could need install dictionaries, if your system doesn't contain any generic dictionary used by enchant
    """
    @staticmethod
    def correct(clPaper):
        """
            :param clPaper:
            :return:
        """
        Corrector.report = ''
        newSections = []
        enDictionary = enchant.Dict("en_US")
        for section in clPaper.sections:
            newSection = []
            for sentence in section:
                newSentence = ''
                sentenceWords = word_tokenize(sentence)
                for word in sentenceWords:
                    if Corrector.shouldCorrect(word):
                        wordIndex = sentenceWords.index(word)
                        # Divided word situation, ex. struct -ure
                        if (wordIndex < (len(sentenceWords) - 1)) and not enDictionary.check(sentenceWords[wordIndex + 1]):
                            composedWord = word + sentenceWords[wordIndex + 1]
                            if enDictionary.check(composedWord):
                                Corrector.report += ' word : ' + composedWord + ' is fixed ! '
                                word = composedWord
                        Corrector.report += word + ' : ' + str(enDictionary.suggest(word)) + '\n'
                        if len(enDictionary.suggest(word)) > 0:
                            word = enDictionary.suggest(word)[0]
                    newSentence += ' ' + word
                newSection.append(newSentence)
            newSections.append(newSection)
        print Corrector.report
        return newSections

    @staticmethod
    def shouldCorrect(word):
        """
            Checking according to a couple of conditions if we shoulf use the correction or not
            :param word:
            :return:
        """
        enDictionary = enchant.Dict("en_US")
        if not enDictionary.check(word) and len(word) > 3 and word.lower() == word and '-' not in word:
            return True
        return False
