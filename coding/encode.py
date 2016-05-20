import xml.etree.ElementTree
import xml.etree.ElementTree
import xml.etree.cElementTree as ET

import editdistance
import enchant
from nltk import word_tokenize


class Corrector:
    """
        :Note for resolving the import issue, you have to install the Lib, for more information:
         http://pythonhosted.org/pyenchant/tutorial.html#installing-the-package
         you could need install dictionaries, if your system doesn't contain any generic dictionary used by enchant
    """

    @staticmethod
    def correct(paperPath):
        """
            this method try to increase the quality of the article before processing it.
            we try to group the devised words such as feat ure.
            and for the words who doesn't exist in the dictionary, we take the suggestions of the suitable words and
            claculate the distance between the word and its alternatives. if the distance is less than 3 then
            we accept the suggestion.

            :param paperPath: the path of the paper.
            :return: the path of the new file.

        """
        paperFile = open(paperPath)
        content = paperFile.read()
        root = xml.etree.ElementTree.fromstring("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + content)
        enDictionary = enchant.Dict("en_US")
        mdText = ''
        sectionIndex = 0
        for section in root:
            mdSection = '## section ' + str(sectionIndex) + '\n'
            sectionIndex += 1
            for sentence in section:
                sentenceWords = word_tokenize(sentence.text)
                newSenteceText = ''
                mdSentence = ''
                isComposedWord = False
                for word in sentenceWords:
                    mdWord = word
                    if not isComposedWord:
                        if Corrector.shouldCorrect(word):
                            wordIndex = sentenceWords.index(word)
                            # Divided word situation, ex. struct -ure
                            if (wordIndex < (len(sentenceWords) - 1)) and not enDictionary.check(
                                    sentenceWords[wordIndex + 1]):
                                composedWord = word + sentenceWords[wordIndex + 1]
                                if enDictionary.check(composedWord):
                                    mdWord = '***' + composedWord + '***( ' + word + ' ' + sentenceWords[
                                        wordIndex + 1] + ')'
                                    word = composedWord
                                isComposedWord = True
                            if len(enDictionary.suggest(word)) > 0:
                                if editdistance.eval(word, enDictionary.suggest(word)[0]) < 4:
                                    mdWord = '**' + enDictionary.suggest(word)[0] + '**( ' + word + ' )'
                                    word = enDictionary.suggest(word)[0]
                        newSenteceText += word + ' '
                        mdSentence += mdWord + ' '

                    else:
                        isComposedWord = False
                sentence.text = newSenteceText
                mdSection += mdSentence + '\n\n'
            mdText += mdSection + '\n\n\n\n\n\n'
        tree = ET.ElementTree(root)
        newPath = paperPath[:-4] + "-correction.xml"
        tree.write(newPath)
        return newPath
        # print mdText


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
