from os import listdir
from os.path import join
import xml.etree.ElementTree as ET
import numpy as np
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

from copy import copy
from sklearn import cross_validation

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
        line=line.split(" | ")
        self.sentencesXml=ET.fromstring("<root>"+line[8][16:]+"</root>")
        self.sentences=[]
        for s in self.sentencesXml.findall('S'):
            self.sentences.append(s.text)
        self.facet=Facet.getIndex(line[9])
    def __str__(self):
        return "S : " + str(self.sentences)+", "+ Facet.getFacet(self.facet)
    def getSentences(self):
        return reduce(lambda x,y:x+y, self.sentences)
    def getFacet(self):
        return Facet.getFacet(self.facet)
        
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
    dict_file=open("words")
    dico=dict()
    for token in dict_file:
        token=token.strip()
        dico[token]=len(dico)
    dict_file.close()
    tokenizer = RegexpTokenizer(r'\w+')
    path="../data"
    trainset=[f for f in listdir(path)]
    matrix=[]
    labels=[]
    clf = MultinomialNB()
    for train in trainset:
        train_file=join(path, train, "annotation", train.split("_")[0]+".annv3.txt")
        annf= AnnotationFile(train_file)
        for ann in annf.getAnnotations():
            vector=np.zeros(len(dico))
            sentences=ann.getSentences()
            s_tokens=tokenizer.tokenize(sentences)
            for t in s_tokens:
                t=t.lower() 
                if t in dico:
                    vector[dico[t]]+=1
            labels.append(ann.getFacet())
            matrix.append(copy(vector))
    clf.fit(matrix, labels)
    
    vector=np.zeros(len(dico))
    words = "Similar to the approach as presented in (Dorow and Widdows, 2003) we construct a word graph".split(" ")
    for w in words :
        w=w.lower()
        if w in dico:
            vector[dico[w]]+=1
    print clf.predict(vector)
    print clf.predict_proba(vector)
    vector=np.zeros(len(dico))
    words = "This paper shows that the combination of a simple feature set made up of bigrams and a standard decision tree learning algorithm results in accurate word sense disambiguation".split(" ")
    for w in words :
        w=w.lower()
        if w in dico:
            vector[dico[w]]+=1
            
    nbFacet=np.zeros(len(Facet.facetList))
    for l in labels:
        nbFacet[Facet.facet[l]]+=1
    for idx, item in enumerate(nbFacet):
        print Facet.facetList[idx], item
    
    scores = cross_validation.cross_val_score(clf, matrix, labels, cv=5)
    print scores
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(matrix, labels, test_size=0.2)
    clf = clf.fit(X_train, y_train)
    y_pred=clf.predict(X_test)
    print clf.score(X_test, y_test)  
    Facet.facetList.sort()
    print(metrics.classification_report(y_test, y_pred))
    