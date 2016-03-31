'''
Created on Mar 31, 2016

@author: dugue
'''
import xml.etree.ElementTree
from nltk import word_tokenize
class FileXml:
    '''
    classdocs
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.path=path
        self.root = xml.etree.ElementTree.parse(self.path).getroot()
        self.num_section=0
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
                self.sectionDesc.append(child.title)
                
    def __str__(self):
        text= self.path + "\nAbstract : "+ str(self.abstract) + "\nSections : " + str(self.sectionDesc)
        for i in range(len(self.sectionDesc)):
            text+="\n Section " + self.sectionDesc[i] + " : "+ str(len(self.sections))
        return text