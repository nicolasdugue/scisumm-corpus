from coding.corpus import Paper
from coding.fm import FeatureMaximization
from coding.matrices import MatricesBuilder


class TextSummarizer:
    """
         Responsible of processing the paper from A to Z.
         it provoke all needed methods form summarizing the paper.
    """
    
    @staticmethod
    def summarize(xmlFilePath):
        """
            Static method responsible of processing the paper from A to Z.
            it provoke all needed methods form summarizing the paper.

            :param xmlFilePath: the relative path of the xml representing the CL Paper we have to summarize
        """
        # Loading the file
        paper = Paper(xmlFilePath)
        # Correcting the encoding problem to enhance the text

        #paper.sections = Corrector.correct(paper)

        # Converting the article sections into arrays
        matricesBuilder = MatricesBuilder(paper)
        # Achieving the feature maximization
        featureMaximizer = FeatureMaximization(matricesBuilder, paper)
        # Getting words which represent and discriminate their sections
        featureMaximizer.getRelevantFeatures()
        # Generating the summary
        summary = []
        for section in paper.getSections():
            for sent in section.getSentences():
                sent.setWeight()
            sortedSen = sorted(section.getSentences(), key=lambda Sentence: Sentence.getWeight(),reverse=True)
            sentNum = int(round((float(section.getSentencesNum()) * 0.05), 0))
            for s in xrange(0, sentNum):
                summary.append(sortedSen[s])
        summary = sorted(summary, key=lambda Sentence: (Sentence.getSection().getSectionIndex(), Sentence.getIndex()))
        # Printing the summary
        for sent in summary:
            print sent
