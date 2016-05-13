from coding.corpus import Paper
from coding.fm import FeatureMaximization
from coding.matrices import MatricesBuilder


class TextSummarizer:
    """
         Responsible of processing the paper from A to Z.
         it provoke all needed methods form summarizing the paper.
    """
    sentencesPercent = 0.05

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

        # TODO: paper.sections = Corrector.correct(paper)

        # Converting the article sections into arrays
        matricesBuilder = MatricesBuilder(paper)
        # Achieving the feature maximization
        featureMaximizer = FeatureMaximization(matricesBuilder, paper)
        # Getting words which represent and discriminate their sections
        featureMaximizer.getRelevantFeatures()
        # Generating the summary

        for section in paper.getSections():
            for sent in section.getSentences():
                sent.setWeight()
        # TODO: Get Text Span

        for ann in paper.getAnnotations():
            print '\n' + 'analysing the annotation ', ann.citanceNumber + '\n'
            for citId, citSent in ann.citingSentencesDictionary.iteritems():
                print '\n' + 'The Citing Sentence ', citSent.getText() + '\n'
                for id, sent in paper.getSentencesDictionary().iteritems():
                    distance = sent.getDistance(citSent)
                    ann.addSpanResultItem(distance, sent, citSent)
                sortedSpanResults = sorted(ann.spanResultList, key=lambda SpanResultItem: SpanResultItem.distance)

                for spanResult in sortedSpanResults[:5]:
                    print str(spanResult).encode('utf-8') + '\n'
        summary = []
        for section in paper.getSections():
            sortedSen = sorted(section.getSentences(), key=lambda Sentence: Sentence.getWeight(),reverse=True)
            sentNum = int(round((float(section.getSentencesNum()) * TextSummarizer.sentencesPercent), 0))
            for s in xrange(0, sentNum):
                summary.append(sortedSen[s])
        summary = sorted(summary, key=lambda Sentence: (Sentence.getSection().getSectionIndex(), Sentence.getIndex()))
        # Printing the summary
        for sent in summary:
            print sent


TextSummarizer.summarize("../data/C90-2039_TRAIN/Citance_XML/C92-1059.xml")
# print file
# print file.getTextFromSection(0)
# print file.getDistributionFromSection(0)
# print file.getDistribution()
# print list(file.getDistributionFromSection(0).values())
# plotter.plotDistrib(list(file.getDistributionFromSection(0).values()))
# plotter.write(file.getDistributionFromSection(0), "../data/C90-2039_TRAIN/Citance_XML/C92-1059.distrib")

# corpus=loader.Corpus("../data")
# print corpus
# corpus.checkXmlOfCited()
# corpus.checkXmlOfCiting()
