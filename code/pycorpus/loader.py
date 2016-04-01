'''
Created on Mar 31, 2016

@author: dugue
'''
import xml.etree.ElementTree
from nltk import word_tokenize
from collections import Counter
from os import listdir
from os.path import join

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
        file=open(path)
        content=""
        self.root=""
        content=file.read()
        self.root = xml.etree.ElementTree.fromstring("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>"+ content)
            
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
        '''
        Return the word distribution of all text
        '''
        text=self.getAllText()
        tokens=word_tokenize(text)
        return Counter(tokens)
    
class Corpus:
    '''
    Allows to handle a whole corpus
    '''

    def __init__(self, path):
        self.citances=[]
        self.cited=[]
        directories=listdir(path)
        for directory in directories:
            list_citances=[f for f in listdir(join(path,directory, "Citance_XML")) if "~" not in f and "xml" in f]
            reference=[f for f in listdir(join(path,directory, "Reference_XML")) if "~" not in f and "xml" in f]
            self.cited.append(join(path,directory, "Reference_XML", reference[0]))
            self.citances.append(map(lambda x: join(path,directory, "Citance_XML", x), list_citances))
        
    def __str__(self):
        return "Citing paper :" + str(self.citances)+"\nCited papers : " + str(self.cited)
    
    def checkXmlOfCited(self):
        for cited in self.cited :
            try :
                FileXml(cited)
            except xml.etree.ElementTree.ParseError as e:
                print cited + " - " + str(e)
                
    def checkXmlOfCiting(self):
        for group_of_citing in self.citances :
            for citances in group_of_citing:
                try :
                    FileXml(citances)
                except xml.etree.ElementTree.ParseError as e:
                    print citances + " - " + str(e)
     