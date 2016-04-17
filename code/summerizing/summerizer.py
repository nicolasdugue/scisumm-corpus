from pycorpus import loader
from nlp import processing
from coding import correcting
from matrices.Builder import MatricesBuilder
import pyfmax.fmax as FeaturesMaximizer


class TextSummerizer:
    
    @staticmethod
    def summerizeXml(xmlFilePath):
        
        xmlFile = loader.XMLFile(xmlFilePath)
        for section in xmlFile.sections :
            sectionIndex = xmlFile.sections.index(section)
            section = xmlFile.getTextFromSection(sectionIndex)
            section = correcting.Corrector.correct(section)
            section = processing.NLPProcessor.processText(section)
        
        wordOccurenceMatrix = MatricesBuilder.buildMatrices(xmlFile)
        clusteringMatrix = MatricesBuilder.getClustersList(xmlFile)
        labelColumn =  MatricesBuilder.getLabelColumn(xmlFile)
        featureMaximizer = FeaturesMaximizer.FeatureMaximizer(wordOccurenceMatrix, clusteringMatrix, labels_col=labelColumn)
        relevantFeatures = featureMaximizer.getRelevantFeatures()
        