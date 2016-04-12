'''
Created on Mar 31, 2016

@author: dugue
'''
from pycorpus import loader, plotter
import nltk

file=loader.FileXml("../data/C90-2039_TRAIN/Citance_XML/C92-1059.xml")
print file
print file.getTextFromSection(0)
print file.getDistributionFromSection(0)
print file.getDistribution()
print list(file.getDistributionFromSection(0).values())
plotter.plotDistrib(list(file.getDistributionFromSection(0).values()))
plotter.write(file.getDistributionFromSection(0), "../data/C90-2039_TRAIN/Citance_XML/C92-1059.distrib")

corpus=loader.Corpus("../data")
print corpus
corpus.checkXmlOfCited()
corpus.checkXmlOfCiting()