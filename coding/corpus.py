"""
    Created on Mar 31, 2016
    @author: dugue, Al Saied
"""
import sys
import re
from os import listdir
from os.path import join
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import xml.etree.ElementTree
from collections import Counter


class Paper:

    def __init__(self, paperPath):
        try:
            paperFile = open(paperPath)
            self.setPaperPath(paperPath)
            content = paperFile.read()
            self.root = xml.etree.ElementTree.fromstring("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + content)
            self.__wordnetLemmatizer = WordNetLemmatizer()
            self.__vocabulary = {}
            self.__sections = []
            self.__sectionNumber = 0
            self.__sentenceNumber = 0
            self.__wordNumber = 0
            sectionIndex = 0
            for child in self.root:
                sentences = []
                if child.tag == 'ABSTRACT':
                    continue
                    # index = 0
                    # for item in child:
                    #     sentences.append(Sentence(index, None, item.text))
                    #     index += 1
                    # self.setAbstract(sentences)
                else:
                    section = Section(sectionIndex, [], self)
                    sentIndex = 0
                    for item in child:
                        sentence = Sentence(sentIndex, section, item.text)
                        section.addSentence(sentence)
                        sentIndex += 1
                    sectionIndex += 1
                    section.setTitle(child.get("title"))
                    self.addSection(section)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def setAbstract(self, sentences):
        self.__abstractSentences = sentences

    def getAbstract(self):
        return self.__abstractSentences

    def setPaperPath(self, path):
        self.__paperPath = path

    def getPaperPath(self):
        return self.__paperPath

    def setSections(self, secs):
        self.__sections = secs

    def getSections(self):
        return self.__sections

    def getSectionsNum(self):
        return len(self.__sections)

    def addSection(self, section):
        self.__sectionNumber += 1
        self.__sections.append(section)

    def addToVocabulary(self, word):
        self.__vocabulary[word.getLemma().lower()] = word

    def isInVocabulary(self, wordForm):
        lemma = self.__wordnetLemmatizer.lemmatize(wordForm)
        if lemma in self.__vocabulary.keys():
            return True
        return False

    def getWordFromVocabulary(self,wordForm):
        lemma = self.__wordnetLemmatizer.lemmatize(wordForm)
        if lemma in self.__vocabulary:
            return self.__vocabulary[lemma]
        return None

    def increaseSentenceNumber(self):
        self.__sentenceNumber += 1

    def increaseWordNumber(self):
        self.__wordNumber += 1


class Section:
    def __init__(self, sectionIndex, sentences, paper):
        self.setSectionIndex(sectionIndex)
        self.__sentences = []
        self.__text = ''
        self.setSentences(sentences)
        self.setPaper(paper)

    def getSectionIndex(self):
        return self.__sectionIndex

    def setSectionIndex(self, sectionIndex):
        self.__sectionIndex = sectionIndex

    def getTitle(self):
        return self.__title

    def setTitle(self, name):
        self.__title = name

    def getPaper(self):
        return self.__paper

    def setPaper(self, paper):
        self.__paper = paper

    def setSentences(self, sens):
        self.__sentences = sens

    def getSentences(self):
        return self.__sentences

    def addSentence(self, sentence):
        self.getPaper().increaseSentenceNumber()
        self.__sentences.append(sentence)

    def getSentencesNum(self):
        return len(self.__sentences)

    def addText(self,text):
        self.__text += text

    def getText(self):
        return self.__text

    def __str__(self):
        return ' the section ' + self.getSectionIndex() + self.getTitle()


class Sentence:
    def __init__(self, index, section, text):
        self.setIndex(index)
        self.setSection(section)
        self.__words = []
        self.__report = ' '
        self.__text = text
        self.__weight = -1
        section.addText(text)
        wordList = word_tokenize(text)
        for item in wordList:
            if self.getSection() is not None and self.getSection().getPaper().isInVocabulary(item.lower()):
                word = self.getSection().getPaper().getWordFromVocabulary(item.lower())
                word.addIndex(wordList.index(item))
                word.addSentence(self)
            else:
                self.addWord(Word(wordList.index(item), self, item, self.getSection().getPaper()) )

    def getIndex(self):
        return self.__index

    def setIndex(self, index):
        self.__index = index

    def getWeight(self):
        if self.__weight != -1:
            self.setWeight()
        return self.__weight

    def setWeight(self):
        sectionIndex = self.getSection().getSectionIndex()
        wordList = self.__words
        counter = 0
        featureNum = 0
        weightBuffer = 0
        self.__weight = 0
        for word in wordList:
            if word.isCandidateFeature():
                counter += 1
            if word.isFeature():
                featureNum += 1
            weightBuffer += word.getWeight(sectionIndex)
        if counter is not 0:
            self.__weight = weightBuffer / counter
        self.__report = ' sent : ' + str(self.__index) + ' sec : ' + str(self.getSection().getSectionIndex())  + ', weight: '\
                        + str(self.__weight) + ', fNum : ' + str(featureNum) + ' candFNum : ' \
                         + str(counter) + ' : ' + str(self.getWordsNum())

    def getSection(self):
        return self.__section

    def setSection(self, section):
        self.__section = section

    def getText(self):
        return self.__text

    def getWords(self):
        return self.__words

    def setWords(self, words):
        self.__words = words

    def addWord(self, word):
        self.getSection().getPaper().increaseWordNumber()
        if self.__words is None:
            self.__words = []
        self.__words.append(word)

    def getWordsNum(self):
        return len(self.__words)

    def __str__(self):
        result = self.__report + '\n' + self.__text + '\n'
        return result.encode("utf-8")


class Word:
    def __init__(self,index, sentence, text, paper):
        self.__indices = []
        self.__sentences = []
        self.__weight = {}
        self.__isFeature = False
        self.addIndex(index)
        self.addSentence(sentence)
        self.setText(text)

        numberPattern = re.compile("[-+]?\d*\.\d+|\d+")
        mixedPattern = re.compile("\w+")
        self.__isNumber = False
        self.__isStop = False
        self.__isMixed = False
        self.__paper = paper
        if numberPattern.match(self.getText()):
            self.setAsNumber()
        elif not mixedPattern.match(self.getText()):
            self.setAsMixed()
        elif self.getText().lower() in stopwords.words('english'):
            self.setAsStop()
        else:
            wordnetLemmatizer = WordNetLemmatizer()
            self.setLemma(wordnetLemmatizer.lemmatize(self.getText()))
            self.getPaper().addToVocabulary(self)

    def getIndices(self):
        return self.__indices

    def setIndices(self, index):
        self.__indices = index

    def addIndex(self, index):
        self.__indices.append(index)

    def setAsNumber(self):
        self.__isNumber = True

    def isNumber(self):
        if self.__isNumber:
            return True
        return False

    def setAsMixed(self):
        self.__isMixed = True

    def isMixed(self):
        if self.__isMixed:
            return True
        return False

    def setAsStop(self):
        self.__isStop = True

    def isStop(self):
        if self.__isStop:
            return True
        return False

    def getText(self):
        return self.__text

    def setText(self, text):
        self.__text = text

    def getLemma(self):
        if self.__lemma is not None:
            return self.__lemma
        return self.__text

    def setLemma(self, text):
        self.__lemma = text

    def getWeight(self, sectionIndex):
        if sectionIndex in self.__weight:
            return self.__weight[sectionIndex]
        return 0

    def setWeight(self, weigh, sectionIndex):
        if sectionIndex not in self.__weight:
            self.__weight[sectionIndex] = weigh

    def getPaper(self):
        return self.__paper

    def setPaper(self, paper):
        self.__paper = paper

    def getSentences(self):
        return self.__sentences

    def setSentences(self, sentences):
        self.__sentences = sentences

    def addSentence(self, sentence):
        if self.__sentences is None:
            self.__sentences = []
        self.__sentences.append(sentence)

    def isCandidateFeature(self):
        if len(self.getText()) < 3 or self.isMixed() or self.isStop() or self.isNumber():
            return False
        return True

    def setAsFeature(self):
        self.__isFeature = True

    def isFeature(self):
        return self.__isFeature

    def __str__(self):
        result = self.getText()
        if self.isMixed():
            result += ' ,Mixed '
        if self.isStop():
            result += ' ,Stop'
        if self.isNumber():
            result += ' ,Number'
        if self.__weight is not None:
            result += ' ,weight: ' + str(self.__weight)
        return result.encode("utf-8")

class CLPaper:
    """
    Allows to load an xml file from the corpus
    """

    def __init__(self, path):
        """
            Constructor
            path is the file path
            root is the xml root of the file
            sections is a list of list. Each item of the list is a section. In each of these items, there is a sublist containing all the sentences
            sectionDesc contains the section names
            abstract is the list of abstract sentences
        """
        self.path = path
        paperFile = open(path)
        content = ""
        self.root = ""
        content = paperFile.read()
        self.root = xml.etree.ElementTree.fromstring("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + content)
        self.sections = []
        self.sectionDesc = []
        self.abstract = []
        for child in self.root:
            if child.tag == 'ABSTRACT':
                for sentences in child:
                    self.abstract.append(sentences.text)
            else:
                section = []
                for sentences in child:
                    section.append(sentences.text)
                self.sections.append(section)
                self.sectionDesc.append(child.get("title"))

    def __str__(self):
        text = self.path + "\nAbstract : " + str(self.abstract) + "\nSections : " + str(self.sectionDesc)
        for i in range(len(self.sectionDesc)):
            text += "\n Section " + self.sectionDesc[i] + " : " + str(len(self.sections[i])) + " sentences recorded"
        return text

    def getTextFromSection(self, i):
        """
            Return the plain text of section i
        """
        return reduce(lambda x, y: x + y, self.sections[i])

    def getDistributionFromSection(self, i):
        """
            Return the word distribution of section i
        """
        text = self.getTextFromSection(i)
        tokens = word_tokenize(text)
        return Counter(tokens)

    def getAllText(self):
        text = ""
        for i in range(len(self.sectionDesc)):
            text += self.getTextFromSection(i)
        return text

    def getDistribution(self):
        """
            Return the word distribution of all text
        """
        text = self.getAllText()
        tokens = word_tokenize(text)
        return Counter(tokens)


class Corpus:
    """
        Allows to handle a whole corpus
    """

    def __init__(self, path):
        self.citances = []
        self.cited = []
        directories = listdir(path)
        for directory in directories:
            list_citances = [f for f in listdir(join(path, directory, "Citance_XML")) if
                             "~" not in f and "xml" in f]
            reference = [f for f in listdir(join(path, directory, "Reference_XML")) if "~" not in f and "xml" in f]
            self.cited.append(join(path, directory, "Reference_XML", reference[0]))
            self.citances.append(map(lambda x: join(path, directory, "Citance_XML", x), list_citances))

    def __str__(self):
        return "Citing paper :" + str(self.citances) + "\nCited papers : " + str(self.cited)

    def checkXmlOfCited(self):
        for cited in self.cited:
            try:
                CLPaper(cited)
            except xml.etree.ElementTree.ParseError as e:
                print cited + " - " + str(e)

    def checkXmlOfCiting(self):
        for group_of_citing in self.citances:
            for citances in group_of_citing:
                try:
                    CLPaper(citances)
                except xml.etree.ElementTree.ParseError as e:
                    print citances + " - " + str(e)