#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.sparse import csr_matrix, csc_matrix

class MatrixClustered:
	"""
		This class allows to define a matrix which rows (objects) were clustered
		Labels can be used to describe rows (objects) and columns (features)
    	"""

	def __init__(self, matrix, clustering, labels_row=[], labels_col=[]):
		"""
		Matrix and clustering should be at least passed.
		Matrix should be a 2D Array or already a sparse (csr or csc) matrix.
		Clustering should be an array where a value v at index i defines that the object i (row i in matrix) belongs to cluster v
		Labels can be used to describe rows (objects) and columns (features) in the same way as the clustering object
    		"""

		self.matrix_csr = csr_matrix(matrix)

		self.matrix_csc = csc_matrix(matrix)

		self.clustering=clustering
		
		self.clusters=[]
		for idx,elmt in enumerate(self.clustering):
			elmt=int(elmt)
			taille=(len(self.clusters) -1) 
			if elmt >= taille:
				for i in range(elmt - taille):
					self.clusters.append([])
			self.clusters[elmt].append(idx)

		self.labels_row=labels_row

		self.labels_col=labels_col

		self.sum_rows=self.matrix_csr.sum(axis=1)

		self.sum_cols=self.matrix_csc.sum(axis=0)

		

	def sum_row(self, i):
		"""
		Get the sum of row i
    		"""
		return self.sum_rows[i]

	def sum_col(self, i):
		"""
		Get the sum of column i
    		"""
		return self.sum_cols[i]

	def __str__(self):
		"""
		toString()
    		"""
		return "Matrix CSR (ordered by rows) :\n" + str(self.matrix_csr)+ "\nMatrix CSC (ordered by columns): \n"+ str(self.matrix_csc) + "\nColumns labels (features) " + str(self.labels_col) + "\nRows labels (objects) " + str(self.labels_row) + "\nClustering :  " + str(self.clustering)+"\nClusters : "+str(self.clusters)
		
