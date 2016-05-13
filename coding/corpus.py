"""
    Created on Mar 31, 2016
    @author: dugue, Al Saied
"""
import math
import re
import sys
import xml.etree.ElementTree
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
from collections import Counter
from os import listdir
from os.path import join

from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy import spatial


class Annotation:
    def __init__(self, annotationText):
        self.spanResultList = []
        self.isValid = True
        annotations = annotationText.split('|')
        self.citingSentences = []
        self.citingSentencesDictionary = {}
        for ann in annotations:
            annList = ann.split(':')
            if len(annList) <= 1:
                continue
            content = ''
            if len(annList) > 2:
                for i in xrange(1, len(annList)):
                    content += annList[i]
            else:
                content = annList[1].strip()
            title = annList[0].strip()
            if title == 'Citance Number':
                self.citanceNumber = content
            elif title == 'Citing Article':
                self.citingArticle = content
            elif title == 'Citation Marker':
                self.citationMarker = content
            elif title == 'Citation Text':
                self.citationText = content
            elif title == 'Reference Text':
                self.referenceText = content
            elif title == 'Discourse Facet':
                self.discourseFacet = content
        self.getCitingSentences()

        # def getNeighborSentences(self, paper):
        # TODO: add the implemmentation
        # sents = self.getCitingSentences()
        # citingPaperPath = self.getCitingPaperPath()

    def getCitingPaperPath(self, paper):
        if paper is not None and paper.getPaperName() is not None and self.citingArticle is not None:
            return '../data/' + paper.getPaperName() + '/citance_XML' + self.citingArticle
        return ''

    def addSpanResultItem(self, distance, sent, citingSent):
        self.spanResultList.append(SpanResultItem(distance, sent, citingSent))

    def getCitingSentences(self):
        if len(self.citingSentences) > 0:
            return self.citingSentences
        try:
            self.root = xml.etree.ElementTree.fromstring(
                "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><citance>" + self.citationText + '</citance>')
        except:
            self.isValid = False
            return
        for child in self.root:
            sentence = Sentence(child.text)
            sentence.setIndex(int(child.attrib['sid']))
            self.citingSentences.append(sentence)
            self.citingSentencesDictionary[int(child.attrib['sid'])] = sentence
        return self.citingSentences


class SpanResultItem:
    def __init__(self, distance, referenceSent, citingSent):
        if math.isnan(distance):
            distance = 1.
        self.distance = distance
        self.referenceSent = referenceSent
        self.referenceSentIndex = referenceSent.getIndex()
        self.citingSentence = citingSent
        self.citingSentIndex = citingSent.getIndex()

    def __str__(self):
        return str(self.distance) + '\n' + 'reference: ' + str(self.referenceSentIndex) + ' : ' \
               + self.referenceSent.getText() + '\n'


class Paper:

    def __init__(self, paperPath):
        try:

            paperFile = open(paperPath)
            self.setPaperPath(paperPath)
            self.setPaperName(paperPath)
            self.setAnnotations(paperPath)
            content = paperFile.read()
            self.root = xml.etree.ElementTree.fromstring("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" + content)
            self.__wordNetLemmatizer = WordNetLemmatizer()
            self.__vocabulary = {}
            self.__SentencesDictionary = {}
            self.__sections = []
            self.__abstractTerms = []
            self.__titleTerms = []
            self.__abstractSentences = []
            self.__sectionNumber = 0
            self.__sentenceNumber = 0
            self.__wordNumber = 0
            sectionIndex = 0
            for child in self.root:
                if child.tag == 'ABSTRACT':
                    index = 0
                    for item in child:
                        self.addAbstractSentence(Sentence(item.text, index, None, True))
                        index += 1
                    # Storing the important words of the abstract
                    for sentence in self.getAbstract():
                        wordList = word_tokenize(sentence.getText())
                        # We use post tagging for overweighting the abstract terms who are nous
                        wordListTagged = pos_tag(wordList)
                        for word in sentence.getWords():
                            for postTag in wordListTagged:
                                if postTag[0].lower() == word.getText().lower() and postTag[1].startswith('NN'):
                                    if word.isCandidateFeature() and not word.exist(self.getAbstractTerm()):
                                        self.addAbstractTerm(word)
                else:
                    section = Section(sectionIndex, [], self)
                    sentIndex = 0
                    for item in child:
                        sentence = Sentence(item.text, item.attrib['sid'], section, False)
                        section.addSentence(sentence)
                        sentIndex += 1
                    sectionIndex += 1
                    section.setTitle(child.get("title"))
                    self.addSection(section)
                    # Storing the important words of sections' titles
                    title = section.getTitle()
                    wordList = word_tokenize(title)
                    # For avoiding the ordinary words, introduction conclusions ..
                    for wordForm in wordList:
                        word = Word(wordForm, None, wordList.index(wordForm), None)
                        if word.isCandidateFeature() and not word.exist(self.getTitleTerm()):
                            self.__titleTerms.append(word)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def setAnnotations(self, paperPath):
        """
            THis method try to read the annotation files of each document of the corpus.
            for each citing paper it store the required data inside @Annotation object

            :param paperPath: the path of the paper
        """
        annPathList = self.getPaperName().split('_')
        annotationPath = '../data/' + self.getPaperName() + '/annotation/' + annPathList[0] + '.annv3.txt'
        try:
            annotationFile = open(annotationPath)
            self.__annotationPath = annotationPath
            self.__annotations = []
            lines = annotationFile.readlines()
            self.createAnnotationXML(lines)
            for line in lines:
                if len(line.split('|')) > 1:
                    self.__annotations.append(Annotation(line))
            annotationFile.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def createAnnotationXML(self, lines):

        root = ET.Element("root")
        for line in lines:
            if len(line.split('|')) > 1:
                citance = ET.SubElement(root, "Citance")
                annotations = line.split('|')
                self.citingSentences = []
                self.citingSentencesDictionary = {}
                for ann in annotations:
                    annList = ann.split(':')
                    if len(annList) <= 1:
                        continue
                    content = ''
                    if len(annList) > 2:
                        for i in xrange(1, len(annList)):
                            content += annList[i]
                    else:
                        content = annList[1].strip()
                    content = str(content)
                    title = annList[0].strip().replace(' ', '_')
                    if 'citation text' in annList[0].lower() or 'reference text' in annList[0].lower():
                        try:
                            citationTextSents = xml.etree.ElementTree.fromstring('<Sents>' + content + '</Sents>')
                            citationText = ET.SubElement(citance, title)
                            for item in citationTextSents.getchildren():
                                sent = ET.SubElement(citationText, item.tag)
                                sent.text = item.text
                                sent.attrib = item.attrib
                        except:
                            print "Unexpected error:", sys.exc_info()[0]
                    else:
                        ET.SubElement(citance, title).text = content
        tree = ET.ElementTree(root)
        tree.write('../data/' + self.getPaperName() + '/annotation/xml' + self.getPaperName() + '.xml')

    def getAnnotations(self):
        """
            Return a list of annotation objects which contain information about the reference paper and the citing papers
        """
        return self.__annotations

    def setAbstract(self, sentences):
        self.__abstractSentences = sentences

    def getAbstract(self):
        return self.__abstractSentences

    def setPaperName(self, path):
        """
            Storing the name of the document , ex 'C90_2093_TRAIN'

            :param path: the path of the paper
        """
        self.__paperName = ''
        getName = False
        pathlist = path.split('/')
        for item in pathlist:
            if getName:
                self.__paperName = item
                break
            if item == 'data':
                getName = True

    def getPaperName(self):
        """
            :return: The name of the paper, ex 'C90_2093_TRAIN'
        """
        return self.__paperName

    def addAbstractSentence(self, sent):
        self.__abstractSentences.append(sent)

    def setAbstractTerm(self, terms):
        self.__abstractTerms = terms

    def getAbstractTerm(self):
        return self.__abstractTerms

    def addAbstractTerm(self, term):
        self.__abstractTerms.append(term)

    def setTitleTerm(self, terms):
        self.__titleTerms = terms

    def getTitleTerm(self):
        return self.__titleTerms

    def addTitleTerms(self, term):
        self.__titleTerms.append(term)

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
        lemma = self.__wordNetLemmatizer.lemmatize(wordForm)
        if lemma in self.__vocabulary.keys():
            return True
        return False

    def getWordFromVocabulary(self, wordForm):
        lemma = self.__wordNetLemmatizer.lemmatize(wordForm)
        if lemma in self.__vocabulary:
            return self.__vocabulary[lemma]
        return None

    def increaseSentenceNumber(self):
        self.__sentenceNumber += 1

    def increaseWordNumber(self):
        self.__wordNumber += 1

    def getSentencesDictionary(self):
        return self.__SentencesDictionary

    def getSentenceByIndex(self, index):
        if index in self.__SentencesDictionary.keys():
            return self.__SentencesDictionary[index]
        return None

    def addToSentenceDictionary(self, sent):
        if sent.getIndex() is not None:
            if self.getSentenceByIndex(sent.getIndex()) is not None:
                print '## Warning: sentences with the same index ', sent.getIndex(), ' : ', sent
            self.__SentencesDictionary[sent.getIndex()] = sent

    def getMaxWeight(self, lemma):
        if lemma in self.__vocabulary:
            word = self.__vocabulary[lemma]
            return word.getMaxWeight()
        return 0


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
    def __init__(self, text, index=None, section=None, isAbstract=None):

        self.__report = ''
        self.__text = text
        self.__words = []
        wordList = word_tokenize(text)
        if section is None and index is None and isAbstract is None:
            for item in wordList:
                self.__words.append(Word(item, self))
        else:
            self.setIndex(index)
            self.__section = section
            self.__weight = -1
            if section is not None:
                section.addText(text)
            if isAbstract:
                for item in wordList:
                    self.addWord(Word(item, self, wordList.index(item), None))
                return

            for item in wordList:
                if self.getSection() is not None and self.getSection().getPaper().isInVocabulary(item.lower()):
                    word = self.getSection().getPaper().getWordFromVocabulary(item.lower())
                    word.addIndex(wordList.index(item))
                    word.addSentence(self)
                    self.addWord(word)
                else:
                    self.addWord(Word(item, self, wordList.index(item), self.getSection().getPaper()))
            if self.getSection() is not None and self.getSection().getPaper() is not None:
                self.getSection().getPaper().addToSentenceDictionary(self)

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
            word.setMaxWeight()
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
        if self.getSection() is not None and self.getSection().getPaper() is not None:
            self.getSection().getPaper().increaseWordNumber()
        self.__words.append(word)

    def getWordsNum(self):
        return len(self.__words)

    def getImportantLength(self):
        length = 0
        for word in self.getWords():
            if word.isCandidateFeature():
                length += 1
        return length

    def getLemmaList(self):
        lemma = []
        for word in self.getWords():
            if word.isCandidateFeature():
                lemma.append(word.getLemma())
        return lemma

    def getDistance(self, citingSent):
        """
            This method is sed to calculate the distance between two sentences using the cosine similarity measure
             and the weights of the two sentences' words according to the feature maximiwation on the article.
        :param citingSent: the sentence mentioned in the citance
        :return: the distance between two sentences
        """
        wordWeightDic = {}
        # sent = Sentence(sentenceStr)
        # Creating weights for the words of the given sentence
        for word in citingSent.getWords():
            word.updateMaxWeight(self.getSection().getPaper().getMaxWeight(word.getLemma()))
            wordWeightDic[word.getLemma()] = word.getMaxWeight()

        firstVector = []
        secondVector = []
        firstLemmaList = self.getLemmaList()
        secondLemmaList = citingSent.getLemmaList()

        for word in self.getWords():
            if word.isCandidateFeature():
                firstVector.append(word.getWeight(self.getSection().getSectionIndex()))
                if word.getLemma() in secondLemmaList:
                    if word.getLemma() in wordWeightDic.keys():
                        secondVector.append(wordWeightDic[word.getLemma()])
                    else:
                        secondVector.append(0)
                else:
                    secondVector.append(0)

        for word in citingSent.getWords():
            if word.isCandidateFeature():
                if word.getLemma() not in firstLemmaList:
                    firstVector.append(0)
                    if word.getLemma() in wordWeightDic.keys():
                        secondVector.append(wordWeightDic[word.getLemma()])
                    else:
                        secondVector.append(0)

        return spatial.distance.cosine(firstVector, secondVector)

    def __str__(self):
        result = self.__report + '\n' + self.__text + '\n'
        return result.encode("utf-8")


class Word:
    sentencesPercent = 0.05
    titleWordWeight = 1.2
    abstractWordWeight = 1.2

    # The main initiator
    def __init__(self, text, sentence, index=None, paper=None):

        self.__indices = []
        self.__sentences = []
        self.__weight = {}
        self.__maxWeight = 0
        self.__isFeature = False
        self.__isContrastFeature = False
        self.__isAbstractWord = False
        self.__isTitleWord = False
        if index is not None:
            self.addIndex(index)
        self.addSentence(sentence)
        self.setText(text)
        self.__maxWeight = 0
        numberPattern = re.compile("[-+]?\d*\.\d+|\d+")
        mixedPattern = re.compile("\w+")
        self.__isNumber = False
        self.__isStop = False
        self.__isMixed = False
        if paper is not None:
            self.__paper = paper
        self.__lemma = ''
        if numberPattern.match(self.getText()):
            self.setAsNumber()
        elif not mixedPattern.match(self.getText()):
            self.setAsMixed()
        elif self.getText().lower() in stopwords.words('english'):
            self.setAsStop()
        else:
            wordnetLemmatizer = WordNetLemmatizer()
            self.setLemma(wordnetLemmatizer.lemmatize(self.getText()))
            if paper is not None:
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
        if self.__lemma != '':
            return self.__lemma
        return self.__text

    def setLemma(self, text):
        self.__lemma = text.lower()

    def getWeight(self, sectionIndex):
        if sectionIndex in self.__weight:
            return self.__weight[sectionIndex]
        return 0

    def setWeight(self, weigh, sectionIndex):
        if sectionIndex not in self.__weight:
            paper = self.getSentences()[0].getSection().getPaper()
            if self.exist(paper.getAbstractTerm()):
                weigh *= Word.abstractWordWeight
                self.__isAbstractWord = True
            if self.exist(paper.getTitleTerm()):
                weigh *= Word.titleWordWeight
                self.__isTitleWord = True
            self.__weight[sectionIndex] = weigh

    def setMaxWeight(self):
        if self.isCandidateFeature() and self.__weight.values():
            self.__maxWeight = max(self.__weight.values())

    def updateMaxWeight(self, w):
        self.__maxWeight = w

    def getMaxWeight(self):
        return self.__maxWeight

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

    def setAsContrastFeature(self):
        self.__isContrastFeature = True

    def isContrastFeature(self):
        return self.__isContrastFeature

    def exist(self, list):
        for word in list:
            if word.getLemma() == self.getLemma():
                return True
        return False

    def __str__(self):
        result = self.getText()
        if self.__isContrastFeature:
            result += ' ,Contrast '
        if self.__isFeature:
            result += ' ,Feature '
        if self.__isAbstractWord:
            result += ' ,Abstract '
        if self.__isTitleWord:
            result += ' ,Title '
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