import numpy as np


class FM:
    def __init__(self, matricesBuilder):
        self.occurrenceArray = np.asarray(matricesBuilder.occurrenceArray)
        self.vocabulary = matricesBuilder.vocabulary
        self.columnSum = self.__getColSum()
        self.rowSum = self.__getRowSum()
        self.fr = self.fp = self.ff = []
        self.__generateFRarr()
        self.__generateFParr()
        self.__generateFFarr()
        self.clustersCardinality = self.__calculateClustersCardinality()
        self.hatedFFf = self.__calculateHatedFFf()
        self.hatedFFd = self.__calculateHatedFFd()

    def getRelevantFeatures(self):
        """
            get features which represent and discriminate classes

            Returns
            -------
                 boolean array whose row are indices of the classes and columns are features
                 if result[clusterIndex, featureIndex] is true then the feature represent and discriminate the class
        """
        result = []
        # iteration over classes
        for clusterIndex in xrange(0, len(self.occurrenceArray)):
            resultRow = []
            # iteration over features
            for featureIndex in xrange(0, len(self.occurrenceArray[0])):
                FF = self.ff[clusterIndex][featureIndex]
                if FF > self.hatedFFf[featureIndex] and FF > self.hatedFFd:
                    print 'The word ', self.vocabulary.keys()[
                        featureIndex], 'is relevant for the section ', clusterIndex
                    resultRow.append(True)
                else:
                    resultRow.append(False)
            result.append(resultRow)
        return result

    def __calculateHatedFFf(self):
        """
            Calculate the hated FFd for a given feature

            Returns
            -------
                  the value of hated FFd for a given feature
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

            Returns
            -------
                  the value of hated  FFd for all features
        """
        # iteration over features
        tempSum = 0
        for featureIndex in xrange(0, len(self.occurrenceArray[0])):
            tempSum += self.hatedFFf[featureIndex]
        return tempSum / len(self.occurrenceArray[0])

    def __generateFRarr(self):
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
        for i in xrange(0, len(self.occurrenceArray)):
            row = []
            for j in xrange(0, len(self.occurrenceArray[0])):
                if self.fr[i][j] + self.fp[i][j] != 0:
                    row.append(2 * self.fr[i][j] * self.fp[i][j] / (self.fr[i][j] + self.fp[i][j]))
                else:
                    row.append(0)
            self.ff.append(row)
        return self.ff

    def __calculateClustersCardinality(self):
        """
            Calculate the cardinality of clusters for all the feature

            Returns
            -------
                  the cardinality of clusters for a given feature
        """
        result = []
        for word in self.vocabulary:
            result.append(len(self.vocabulary[word]))
        return result

    def __getColSum(self):
        result = []
        for i in xrange(0, len(self.occurrenceArray[0])):
            tempSum = 0
            for j in xrange(0, len(self.occurrenceArray)):
                tempSum += self.occurrenceArray[j][i]
            result.append(tempSum)
        return result

    def __getRowSum(self):
        result = []
        for i in xrange(0, len(self.occurrenceArray)):
            tempSum = 0
            for j in xrange(0, len(self.occurrenceArray[0])):
                tempSum += self.occurrenceArray[i][j]
            result.append(tempSum)
        return result
