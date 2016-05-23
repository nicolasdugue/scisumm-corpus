from os import listdir
from os.path import join
import xml.etree.ElementTree as ET
import textmining


class Facet:
    facet=dict()
    facetList=[]
    facet["Discourse Facet:  Implication_Citation"]=0
    facetList.append("Discourse Facet:  Implication_Citation")
    facet["Discourse Facet:  Method_Citation"]=1
    facetList.append("Discourse Facet:  Method_Citation")
    facet["Discourse Facet:  Aim_Citation"]=2
    facetList.append("Discourse Facet:  Aim_Citation")
    facet["Discourse Facet:  Hypothesis_Citation"]=3
    facetList.append("Discourse Facet:  Hypothesis_Citation")
    facet["Discourse Facet:  Results_Citation"]=4
    facetList.append("Discourse Facet:  Results_Citation")
        
    @staticmethod
    def getIndex(discourse_facet):
        return Facet.facet[discourse_facet.strip()]
    @staticmethod
    def getFacet(index):
        return Facet.facetList[index]

class Annotation:
    def __init__(self, line):
        line=line.split("|")
        self.sentencesXml=ET.fromstring("<root>"+line[8][16:]+"</root>")
        self.sentences=[]
        for s in self.sentencesXml.findall('S'):
            self.sentences.append(s.text)
        self.facet=Facet.getIndex(line[9])
    def __str__(self):
        return "S : " + str(self.sentences)+", "+ Facet.getFacet(self.facet)
    def getSentences(self):
        return reduce(lambda x,y:x+y, self.sentences)
        
class AnnotationFile:
    def __init__(self, path):
        anf=open(path)
        self.annotations=[]
        for line in anf:
            if "C" in line:
                self.annotations.append(Annotation(line))
                
    def getAnnotations(self):
        return self.annotations
    def __str__(self):
        chaine=""
        for ann in self.annotations:
            chaine+=str(ann)+"\n"
        return chaine

if __name__ == '__main__':
    path="../data"
    trainset=[f for f in listdir(path)]
    train_files=[]
    for train in trainset:
        train_file=join(path, train, "annotation", train.split("_")[0]+".annv3.txt")
        train_files.append(train_file)
    annf= AnnotationFile(train_file)
    tdm = textmining.TermDocumentMatrix()
    for ann in annf.getAnnotations():
        tdm.add_doc(ann.getSentences())
    tdm.bigram_collocations(
    for row in tdm.rows(cutoff=1):
            print row
       