#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.sparse import csr_matrix, csc_matrix
from scipy.optimize.optimize import Result
import numpy as np


class FeatureMaximizer:
    """
        This class allows to define a matrix which rows (objects) were clustered
        Labels can be used to describe rows (objects) and columns (features)
    """

    def __init__(self, matricesBuilder):
        """
            Matrix and clustering should be at least passed.
            Matrix should be a 2D Array or already a sparse (csr or csc) matrix.
            Clustering should be an array where a value v at index i defines that the object i (row i in matrix) belongs to cluster v
            Labels can be used to describe rows (objects) and columns (features) in the same way as the clustering object
        """
        self.occuranceArray = np.asarray(matricesBuilder.occuranceArray)
        self.matrix_csc = csc_matrix(matricesBuilder.occuranceArray)
        self.matrix_csr = csr_matrix(matricesBuilder.occuranceArray)
        self.clustering = matricesBuilder.sectionsArray
        self.vocabulary = matricesBuilder.vocabulary
        self.labels_col = matricesBuilder.vocabulary.keys()
        self.labels_row = matricesBuilder.sectionsNamesArray

        self.clusters = []
        for idx, elmt in enumerate(self.clustering):
            elmt = int(elmt)
            taille = (len(self.clusters) - 1)
            if elmt >= taille:
                for i in range(elmt - taille):
                    self.clusters.append([])
            self.clusters[elmt].append(idx)

        self.sum_rows = self.matrix_csr.sum(axis=1)
        self.sum_cols = self.matrix_csc.sum(axis=0)
        self.fMeasureArray = self.calculateAllFF()

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
        self.clustersCardinality = self.__calculate_clusters_cardinality()
        self.hatedFFf = self.__calculateHatedFFf()
        self.hatedFFd = self.__calculateHatedFFd()
        # iteration over classes
        for clusterIndex in xrange(0, len(self.clusters)):
            resultRow = []
            # iteration over features
            for featureIndex in xrange(0, len(self.labels_col)):
                FF = fMeasureArray[clusterIndex][featureIndex]
                if FF > self.hatedFFf[featureIndex] and FF > self.hatedFFd:
                    print 'The word ' + self.labels_col[featureIndex] + 'is relevant for the section ' + \
                          self.labels_row[clusterIndex]
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
        for clusterIndex in xrange(0, len(self.clusters)):
            clusterRow = []
            for featureIndex in xrange(0, len(self.labels_col)):
                ff = self.__calculateFF(featureIndex, clusterIndex)
                if ff == 0:
                    clusterRow.append(0)
                else:
                    clusterRow.append(ff)
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
        print 'calculating ff'
        FPrecision = self.__calculateFP(featureIndex, clusterNum)
        FRecall = (self.__calculateFR(featureIndex, clusterNum))[0][featureIndex]
        FRecall = np.asarray(FRecall)[0][featureIndex]
        return 2 * FRecall * FPrecision / (FRecall + FPrecision)

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
        return (float(self.__sumFeatureForCluster(clusterNum, featureIndex)))  /self.__sum_col(featureIndex)

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
        print 'calculating FP'
        fp = float(self.__sumFeatureForCluster(clusterNum, featureIndex)) / self.__sum_cluster(clusterNum)[0, 0]
        print fp
        return fp

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
        for featureIndex in xrange(0, len(self.labels_col)):
            tempSum = 0
            for cluster in self.clusters:
                tempSum += self.__calculateFF(featureIndex, self.clusters.index(cluster))
            tepResult = (tempSum / self.clustersCardinality[featureIndex])
            if tepResult == 0:
                rowResult.append(0)
            else:
                rowResult.append(tepResult[0, 0])
            # result.append(rowResult)
        return rowResult

    def __calculate_clusters_cardinality(self):
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
        for word in self.vocabulary :
            result.append(len(self.vocabulary[word]))
        # result = []
        # for featureIndex in xrange(0, len(self.labels_col)):
        #     cardinality = 0
        #     for cluster in self.clusters:
        #         for row in cluster:
        #             if self.matrix_csc[row, featureIndex] != 0:
        #                 cardinality += 1
        #                 break
        #     result.append(cardinality)
        return result

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
        return np.asarray(self.sum_cols)[i]

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
        return self.occuranceArray[clusterNum][featureIndex]
        # cluster = self.clusters[clusterNum]
        # sum = 0
        # for row in cluster:
        #     sum += self.matrix_csc[row, featureIndex]
        # return sum

    def __str__(self):
        """
            toString()
        """
        return "Matrix CSR (ordered by rows) :\n" + str(
            self.matrix_csr) + "\nMatrix CSC (ordered by columns): \n" + str(
            self.matrix_csc) + "\nColumns labels (features) " + str(self.labels_col) + "\nRows labels (objects) " + str(
            self.labels_row) + "\nClustering :  " + str(self.clustering) + "\nClusters : " + str(self.clusters)
