'''
Created on Mar 31, 2016

@author: dugue
'''
from pycorpus import loader

file=loader.FileXml("../data/C90-2039_TRAIN/Citance_XML/C92-1059.xml")
print file
print file.getTextFromSection(0)
print file.getDistributionFromSection(0)
print file.getDistribution()