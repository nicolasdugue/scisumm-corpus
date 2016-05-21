#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Include the fmax file of package pyfmax using fm namespace
import pyfmax.FeatureMax as fm
#import numpy lib using np namespace
import numpy as np

#Load the file as a 1D array
clustering=np.loadtxt("exemple_isko/clustering_isko")
labels_col=[]
#Read the labels of columns (features)
labels=open("exemple_isko/label_isko")
for ligne in labels:
	labels_col.append(ligne.strip())
#Load the file as a 2D array
matrix=np.loadtxt("exemple_isko/matrix_isko")

#Create a MatrixClustered object using fm namespace which refers to fmax.py in package pyfmax
obj = fm.fmax(matrix, clustering,labels_col=labels_col)
print obj
print 'the first step has finished'
print obj.getRelevantFeatures()
print obj.calculateAllFF()
