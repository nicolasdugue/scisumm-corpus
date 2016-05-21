import sys

from coding.corpus import Paper
from coding.fm import FeatureMaximization
from coding.matrices import MatricesBuilder
from encode import Corrector


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
        # Correcting the encoding problem to enhance the text
        newPaperPath = Corrector.correct(xmlFilePath)
        # Loading the corrected file
        paper = Paper(newPaperPath)
        # Converting the article sections into arrays
        matricesBuilder = MatricesBuilder(paper)
        # Achieving the feature maximization
        featureMaximizer = FeatureMaximization(matricesBuilder, paper)
        # Getting words which represent and discriminate their sections
        featureMaximizer.getRelevantFeatures()
        # assigning weights for sentences using the weight of words
        TextSummarizer.getSentencesWeights(paper)
        # Generating the summary
        TextSummarizer.getSummary(paper)
        # getting the matching sentences with the citance sentences
        TextSummarizer.getInteractiveSummary(paper)

    @staticmethod
    def getSentencesWeights(paper):
        """
            After assigning weights for all the words of the article, we assign weights for sentences in calculating the
            average of informative words for each sentence.

            :param paper:  the article after weighting words.
        """
        for section in paper.getSections():
            for sent in section.getSentences():
                sent.setWeight(section.getSectionIndex())

    @staticmethod
    def getSummary(paper):
        """
            this method is responsible of selecting the most important sentences of the article.
            the important sentence is the sentence which contains more  than 10 informative words, and whose weight is the bigger.
             we choose 5% of the sentences of the articles according previous conditions.

            :param paper:  the article after weighting words and sentences.
            :return: a list of @sentence objects.
        """
        # selecting the most important sentences,
        summarySents = []
        for section in paper.getSections():
            sectionIndex = section.getSectionIndex()
            # Removing the invalid sentences, which contain a lot of distorted words
            for sent in section.getSentences():
                if not sent.isValid():
                    section.getSentences().remove(sent)

            sortedSen = sorted(section.getSentences(), key=lambda Sentence: Sentence.getWeight(sectionIndex),
                               reverse=True)
            sentNum = int(round((float(section.getSentencesNum()) * TextSummarizer.sentencesPercent), 0))
            counter = 0
            # Sentences should also be long enough.
            for s in xrange(0, len(sortedSen)):
                if sortedSen[s].getUsefulWordsNum() > 10:
                    summarySents.append(sortedSen[s])
                    counter += 1
                if counter == sentNum:
                    break
        summarySents = sorted(summarySents, key=lambda Sentence: (
            Sentence.getSection().getSectionIndex(), Sentence.getIndex()))
        # Printing the summary
        summary = '#The Summary\n**ze take 5 percent of the important and long sentences for making the summary**\n\n'
        for sent in summarySents:
            summary += sent.getText() + "\n" + "\n"
        print summary
        return summarySents

    @staticmethod
    def getInteractiveSummary(paper):
        """
            for each annotation of the paper, this method add a list of @SpanResultItem, sorted using the its distance.

            :param paper: the article after weighting words and sentences
        """

        # TODO: Get Text Span
        annotationsReport = ''
        for ann in paper.getAnnotations():
            annotationsReport += '\n' + '#analysing the annotation ' + ann.citanceNumber + '\n'
            if not ann.isValid:
                annotationsReport += '**Not valid annotation**' + '\n'
            for citId, citSent in ann.citingSentencesDictionary.iteritems():
                annotationsReport += '\n' + '##The Citing Sentences : ' + '\n' + str(citSent) + '\n'
                # annotationsReport += 'The useful words : '
                # for word in citSent.getWords():
                #     if word.isCandidateFeature():
                #         annotationsReport += str(word)
                annotationsReport += '\n' + '###The Corpus Reference Sentences : ' + '\n'
                for id, sent in paper.getSentencesDictionary().iteritems():
                    distance = sent.getDistance(citSent, paper)
                    ann.addSpanResultItem(distance, sent, citSent)
                for sent in ann.referenceSentences:
                    sent.getFakeWeight(paper)
                    citSent.getFakeWeight(paper)
                    dist = citSent.getDistance(sent, paper)
                    annotationsReport += str(dist) + '\n'
                    annotationsReport += '\n' + '\n' + '**' + str(
                        sent.getIndex()) + '** : ' + str(sent) + '\n' + '\n'
                    # annotationsReport += 'The useful words : '
                    # for word in sent.getWords():
                    #     if word.isCandidateFeature():
                    #         annotationsReport += str(word)

                    # TODO: add weights for reference sents
                sortedSpanResults = sorted(ann.spanResultList, key=lambda SpanResultItem: SpanResultItem.distance)
                annotationsReport += '\n' + '###Our Reference Sentences : ' + '\n'
                for spanResult in sortedSpanResults[:5]:
                    annotationsReport += str(spanResult).encode("utf-8") + '\n'
                    sent1 = paper.getSentenceByIndex('41')
                    # sent2 = paper.getSentenceByIndex('102')
                    if citSent.getIndex() == 102:
                        sent1.getDistance(citSent, paper)
        print annotationsReport


reload(sys)
sys.setdefaultencoding('utf8')
TextSummarizer.summarize("../data/C90-2039_TRAIN/Reference_XML/C90-2039.xml")

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
