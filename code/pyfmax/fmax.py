#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.sparse import csr_matrix, csc_matrix
from scipy.optimize.optimize import Result

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
		print self.matrix_csr.toarray()
		print self.matrix_csc.toarray()
		self.sum_rows = self.matrix_csr.sum(axis=1)

		self.sum_cols = self.matrix_csc.sum(axis=0)
		
		self.fMeasureArray = self.calculateAllFF()

	def test(self):
		docs = [["hello", "world", "hello"], ["goodbye", "cruel", "world"]]
		indptr = [0]
		indices = []
		data = []
		vocabulary = {}
		for d in docs:
		    for term in d:
		        index = vocabulary.setdefault(term, len(vocabulary))
		        indices.append(index)
		        data.append(1)
		    indptr.append(len(indices))
		
		csr_matrix((data, indices, indptr), dtype=int).toarray()
	
	def getRelevantFeatures(self):
		"""
		    get features which represent and discriminate classes    
		
			Returns
		    -------	
				 boolean array whose row are indices of the classes and columns are features 
				 if result[clusterIndex, featureIndex] is true then the feature represent and discriminate the class 
    	"""
		result = []  
		fMeasureArray = self.fMeasureArray  # self.calculateAllFF()
		self.clustersCardinality = self.__calculateClustersCardinality()
		self.hatedFFf = self.__calculateHatedFFf()
		self.hatedFFd = self.__calculateHatedFFd()
		# iteration over classes
		for clusterIndex in xrange(0, len(self.clusters)):
			resultRow = []
			# iteration over features
			for featureIndex in xrange(0, len(self.labels_col)):
				FF = fMeasureArray[clusterIndex] [featureIndex] 
				if FF > self.hatedFFf[featureIndex] and FF > self.hatedFFd : 
					resultRow.append(True)
				else: 
					resultRow.append(False)
			result.append(resultRow)
		return result
	
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
				clusterRow.append(self.__calculateFF(featureIndex, clusterIndex)[0, 0])
			ffArray.append(clusterRow)
		return ffArray
	
	def __calculateFF(self, featureIndex, clusterNum):
		"""
		    Calculate Feature F-Measure 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside clusters array

			Returns
		    -------	
				 the Feature F-Measure for the given feature on determined cluster
    	"""
		FPrecision = self.__calculateFP(featureIndex, clusterNum)
		FRecall = self.__calculateFR(featureIndex, clusterNum)
		return  2 * FRecall * FPrecision / (FRecall + FPrecision)
	
	def __calculateFR(self, featureIndex, clusterNum):
		"""
		    Calculate Feature Recall 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside clusters array

			Returns
		    -------	
				 the Feature Recall for the given feature on determined cluster
    	"""
		return  self.__sumFeatureForCluster(clusterNum, featureIndex) / self.__sum_col(0)[0, featureIndex]
	
	def __calculateFP(self, featureIndex, clusterNum):
		"""
		    Calculate Feature Precision 
		
		    Attributes
		    ----------
		   	featureIndex : int 
		   		the index of the given feature inside labels_col array.
		   		
			clusterNum : int 
				the index of the given cluster inside clusters array

			Returns
		    -------	
				 the Feature Precision for the given feature on determined cluster
    	"""
		return self.__sumFeatureForCluster(clusterNum, featureIndex) / self.__sum_cluster(clusterNum) 
		 
	def __calculateHatedFFd(self):
		"""
		    Calculate the hated FFd
	
			Returns
		    -------	
				  the value of hated  FFd for all features 
		"""
		# iteration over features
		tempSum = 0
		for featureIndex in xrange(0, len(self.labels_col)):
			tempSum += self.hatedFFf[featureIndex]
		return tempSum / self.__calculateFeaturesCardinality() 
		
	
	def __calculateHatedFFf(self):
		"""
		    Calculate the hated FFd for a given feature
			
			Attributes
		    ----------
			featureIndex : int 
		   		the index of the given feature inside labels_col array.

			Returns
		    -------	
				  the value of hated FFd for a given feature 
    	"""
		rowResult = []
		for featureIndex in xrange(0,len(self.labels_col)):
			tempSum = 0
			for cluster in self.clusters :
				tempSum += self.__calculateFF(featureIndex, self.clusters.index(cluster))
			tepResult = (tempSum / self.clustersCardinality[featureIndex])
			rowResult.append(tepResult[0,0])
			#result.append(rowResult)
		return rowResult
	
	def __calculateClustersCardinality(self):
		"""
		    Calculate the cardinality of clusters for a given feature
			
			Attributes
		    ----------
			featureIndex : int 
		   		the index of the given feature inside labels_col array.

			Returns
		    -------	
				  the cardinality of clusters for a given feature 
    	"""
		result = []
		for featureIndex in xrange(0,len(self.labels_col)):
			cardinality = 0
			for cluster in self.clusters : 
				for row in cluster :
					if self.matrix_csc[row, featureIndex] != 0 :
						cardinality += 1
						break
			result.append(cardinality)
		return  result
	
	def __calculateFeaturesCardinality(self):
		"""
		    Calculate the cardinality of features

			Returns
		    -------	
				  the cardinality of features 
    	"""
		return len(self.labels_col)
	
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
		
