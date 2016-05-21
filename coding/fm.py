"""
    Created on Mar 31, 2016
    @author: Al Saied
"""
import numpy as np


class FeatureMaximization:
    """
        A specialised implementation of feature maximization used for generating a summary of scientific paper of computational linguistics
    """
    def __init__(self, matricesBuilder, paper):
        """
            :param matricesBuilder: an object who encapsulate the occurrence matrix
            and other auxiliary matrices for achieving the process.

            This method generate matrices with the values of feature recall, feature precision and f-measure
            it's also used to calculate the hated FFd and the hated FFf which could be considered as a ratio for
            determining whether the feature, the word, is representative and discriminative on a section of the paper
        """
        self.paper = paper
        self.report = ' Processing a paper which contains ' + str(len(matricesBuilder.occurrenceArray[0]))
        self.report += ' words and ' + str(len(matricesBuilder.occurrenceArray)) + ' sections' + '\n'
        self.occurrenceArray = np.asarray(matricesBuilder.occurrenceArray)
        self.occurrenceMap = matricesBuilder.occurrenceMap
        self.columnSum = self.__getColSum()
        self.rowSum = self.__getRowSum()
        self.fr = self.__generateFRarr()
        self.fp = self.__generateFParr()
        self.ff = self.__generateFFarr()
        self.clustersCardinality = self.__calculateClustersCardinality()
        self.hatedFFf = self.__calculateHatedFFf()
        self.hatedFFd = self.__calculateHatedFFd()

    def getRelevantFeatures(self):
        """
            Get features which represent and discriminate classes

            :return: boolean array whose row are indices of the classes and columns are features
            if result[clusterIndex, featureIndex] is true then the feature represent and discriminate the class
        """
        result = []
        # iteration over classes
        for clusterIndex in xrange(0, len(self.occurrenceArray)):
            resultRow = []
            # iteration over features
            relevantWord = 0
            for featureIndex in xrange(0, len(self.occurrenceArray[0])):
                FF = self.ff[clusterIndex][featureIndex]
                if FF > self.hatedFFf[featureIndex] and FF > self.hatedFFd:
                    sempStr = str(relevantWord) + ' : The word ' + self.occurrenceMap.keys()[featureIndex] \
                                   + ' is relevant for the section ' + str(clusterIndex) + '\n'
                    self.report += sempStr
                    print sempStr
                    wordObj = self.paper.getWordFromVocabulary(self.occurrenceMap.keys()[featureIndex])
                    if wordObj is not None:
                        wordObj.setAsFeature()
                    relevantWord += 1
                    resultRow.append(True)
                else:
                    resultRow.append(False)
            result.append(resultRow)
        return result

    def __calculateHatedFFf(self):
        """
            Calculate the hated FFd for a given feature

            :return: the value of hated FFd for a given feature
        """
        rowResult = []
        for featureIndex in xrange(0, len(self.occurrenceArray[0])):
            tempSum = 0
            for clusterIndex in xrange(0, len(self.occurrenceArray)):
                tempSum += self.ff[clusterIndex][featureIndex]
            tepResult = float(tempSum) / self.clustersCardinality[featureIndex]
            rowResult.append(tepResult)
        return rowResult

    def __calculateHatedFFd(self):
        """
            Calculate the hated FFd

            :return: the value of hated  FFd for all features
        """
        # iteration over features
        tempSum = 0
        for featureIndex in xrange(0, len(self.occurrenceArray[0])):
            tempSum += self.hatedFFf[featureIndex]
        return tempSum / len(self.occurrenceArray[0])

    def __generateFRarr(self):
        """
            Generate matrices with the values of Feature Recall.

            :return: a matrix with the same dimension of the occurrence array where each cell contains
            the value of recall of the word J on the section I
        """
        self.fr = []
        for i in xrange(0, len(self.occurrenceArray)):
            row = []
            for j in xrange(0, len(self.occurrenceArray[0])):
                if self.occurrenceArray[i][j] != 0:
                    row.append(float(self.occurrenceArray[i][j]) / self.columnSum[j])
                else:
                    row.append(0)
            self.fr.append(row)
        return self.fr

    def __generateFParr(self):
        """
            Generate matrices with the values of Feature Precision.

            :return: a matrix with the same dimension of the occurrence array where each cell contains
            the value of Feature Precision of the word J on the section I
        """
        self.fp = []
        for i in xrange(0, len(self.occurrenceArray)):
            row = []
            for j in xrange(0, len(self.occurrenceArray[0])):
                if self.occurrenceArray[i][j] != 0:
                    row.append(float(self.occurrenceArray[i][j]) / self.rowSum[i])
                else:
                    row.append(0)
            self.fp.append(row)
        return self.fp

    def __generateFFarr(self):
        """
            Generate matrices with the values of Feature Measure.

            :return: a matrix with the same dimension of the occurrence array where each cell contains
            the value of F-Measure of the word J on the section I
        """
        self.ff = []
        for i in xrange(0, len(self.occurrenceArray)):
            row = []
            for j in xrange(0, len(self.occurrenceArray[0])):
                ff = 0
                if self.fr[i][j] + self.fp[i][j] != 0:
                    ff = 2 * self.fr[i][j] * self.fp[i][j] / (self.fr[i][j] + self.fp[i][j])
                row.append(ff)
                wordObj = self.paper.getWordFromVocabulary(self.occurrenceMap.keys()[j])
                if wordObj is not None:
                    wordObj.setWeight(ff, i)
            self.ff.append(row)
        return self.ff

    def __calculateClustersCardinality(self):
        """
            Calculate the cardinality of clusters for all the feature.

            :return:the cardinality of clusters for a given feature
        """
        result = []
        for word in self.occurrenceMap:
            result.append(len(self.occurrenceMap[word]))
        return result

    def __getColSum(self):
        """
            Calculate the sum of occurrence of each word for each section.

            :return: an one dimension array equal to the number of features, words.
             each cell contains the number of occurrences of the word I over all sections of the paper
        """
        result = []
        for i in xrange(0, len(self.occurrenceArray[0])):
            tempSum = 0
            for j in xrange(0, len(self.occurrenceArray)):
                tempSum += self.occurrenceArray[j][i]
            result.append(tempSum)
        return result

    def __getRowSum(self):
        """
            Calculate the sum of occurrence of each word for each section.

            :return: an one dimension array equal to the number of sections.
             each cell contains the number of occurrences of all words over each section of the paper
        """
        result = []
        for i in xrange(0, len(self.occurrenceArray)):
            tempSum = 0
            for j in xrange(0, len(self.occurrenceArray[0])):
                tempSum += self.occurrenceArray[i][j]
            result.append(tempSum)
        return result
