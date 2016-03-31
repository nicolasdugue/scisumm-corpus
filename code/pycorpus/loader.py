'''
Created on Mar 31, 2016

@author: dugue
'''
import xml.etree.ElementTree
from nltk import word_tokenize
from collections import Counter

class FileXml:
    '''
    Allows to load an xml file from the corpus
    '''


    def __init__(self, path):
        '''
        Constructor
        path is the file path
        root is the xml root of the file
        sections is a list of list. Each item of the list is a section. In each of these items, there is a sublist containing all the sentences
        sectionDesc contains the section names
        abstract is the list of abstract sentences
        '''
        self.path=path
        self.root = xml.etree.ElementTree.parse(self.path).getroot()
        self.sections=[]
        self.sectionDesc=[]
        self.abstract=[]
        for child in self.root:
            if child.tag == 'ABSTRACT':
                for sentences in child:
                     self.abstract.append(sentences.text)
            else:
                section=[]
                for sentences in child:
                    section.append(sentences.text)
                self.sections.append(section)
                self.sectionDesc.append(child.get("title"))
                
    def __str__(self):
        text= self.path + "\nAbstract : "+ str(self.abstract) + "\nSections : " + str(self.sectionDesc)
        for i in range(len(self.sectionDesc)):
            text+="\n Section " + self.sectionDesc[i] + " : "+ str(len(self.sections[i])) + " sentences recorded"
        return text
    
    def getTextFromSection(self,i):
        '''
        Return the plain text of section i
        '''
        return reduce(lambda x, y: x+y, self.sections[i])
    
    def getDistributionFromSection(self,i):
        '''
        Return the word distribution of section i
        '''
        text=self.getTextFromSection(i)
        tokens=word_tokenize(text)
        return Counter(tokens)
    
    def getAllText(self):
        text=""
        for i in range(len(self.sectionDesc)):
            text+= self.getTextFromSection(i)
        return text
    
    def getDistribution(self):
        text=self.getAllText()
        tokens=word_tokenize(text)
        return Counter(tokens)