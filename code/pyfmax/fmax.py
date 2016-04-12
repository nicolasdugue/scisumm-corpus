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

		self.clustering = clustering
		
		self.clusters = []
		for idx, elmt in enumerate(self.clustering):
			elmt = int(elmt)
			taille = (len(self.clusters) - 1) 
			if elmt >= taille:
				for i in range(elmt - taille):
					self.clusters.append([])
			self.clusters[elmt].append(idx)

		self.labels_row = labels_row

		self.labels_col = labels_col

		self.sum_rows = self.matrix_csr.sum(axis=1)

		self.sum_cols = self.matrix_csc.sum(axis=0)

	def calculateFR(self, featureIndex, clusterNum):
		"""
		    Calculate Feature Recall 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside @clusters array

			Returns
		    -------	
				 the Feature Recall for the given feature on determined cluster
    	"""
		return  self.__sumFeatureForCluster(clusterNum, featureIndex) / self.__sum_col(0)[0, featureIndex]
	
	def calculateFP(self, featureIndex, clusterNum):
		"""
		    Calculate Feature Precision 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside @clusters array

			Returns
		    -------	
				 the Feature Precision for the given feature on determined cluster
    	"""
		return self.__sumFeatureForCluster(clusterNum, featureIndex) / self.__sum_cluster(clusterNum) 
	
	def calculateFF(self, featureIndex, clusterNum):
		"""
		    Calculate Feature F-Measure 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside @clusters array

			Returns
		    -------	
				 the Feature F-Measure for the given feature on determined cluster
    	"""
		FPrecision = self.calculateFP(featureIndex, clusterNum)
		FRecall = self.calculateFR(featureIndex, clusterNum)
		return  2 * FRecall * FPrecision / (FRecall + FPrecision)
	
	def calculateAllFF(self):
		"""
		    Calculate Feature F-Measure for all features on all clusters  
		
			Returns
		    -------	
				 A two dimensions array for Features F-Measure where row index refers to  the cluster 
				 and the column index refers to the feature. 
				 
    	"""	
		ffArray = []
		for clusterIndex in xrange(0, len(self.clusters)) :
			clusterRow = []
			for featureIndex in xrange(0, len(self.labels_col)) :
				clusterRow.append(self.calculateFF(featureIndex, clusterIndex)[0, 0])
			ffArray.append(clusterRow)
		return ffArray
		 
	def __sum_row(self, i):
		"""
			Auxiliary Function.
			Return the sum of row i
    	"""
		return self.sum_rows[i]

	def __sum_col(self, i):
		"""
			Return the value of the sum of all clustering matrix objects for the given feature.
			Used for calculating Precision (Predominance)
    	"""
		return self.sum_cols[i]
	
	def __sum_cluster(self, i):
		"""
			Return the sum of all clustering matrix features for objects belong to the given cluster i.
			Used for calculating feature recall
    	"""
		cluster = self.clusters[i]
		sum = 0
		for row in cluster:
			sum += self.__sum_row(row)
		return sum
    
	def __sumFeatureForCluster(self, clusterNum, featureIndex):
		"""
		    Sum up sub-column, using given cluster on a given feature.  
		
		    Attributes
		    ----------
			clusterNum : int 
				the index of the given cluster inside @clusters array
			
			featureIndex : int 
		   		the index of the given feature inside labels_col array.

			Returns
		    -------	
				 the sum of values for crossing a feature with a cluster 
    	"""
		cluster = self.clusters[clusterNum]
		sum = 0
		for row in cluster:
			sum += self.matrix_csc[row, featureIndex] 
		return sum

	def __str__(self):
		"""
			toString()
    	"""
		return "Matrix CSR (ordered by rows) :\n" + str(self.matrix_csr) + "\nMatrix CSC (ordered by columns): \n" + str(self.matrix_csc) + "\nColumns labels (features) " + str(self.labels_col) + "\nRows labels (objects) " + str(self.labels_row) + "\nClustering :  " + str(self.clustering) + "\nClusters : " + str(self.clusters)
		
