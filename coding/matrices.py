"""
    Created on Mar 31, 2016
    @author: Al Saied
"""
from nltk import word_tokenize


class MatricesBuilder:
    """
        The responsible of reading the computational linguistics paper,
        tokenizing its text, and generating the occurrence array of the paper.

        The object of this class is used to encapsulate the occurrence array
        of the passed article to the feature maximizatin
    """
    titleWords = []

    def __init__(self, paper):
        """

        :param paper: Computational linguistic paper, scientific article

        for more info: @coding.corpus.CLPaper
        The initialization process is used to give values for the following variables :

            self.occurrenceArray:       array of section index over rows and word index over columns
            self.sectionsArray:         integer index of the available sections
            self.sectionsNamesArray:    the textual title of sections
            self.vocabulary:            Dictionary with key: word, values: dictionary of sections indices
                                        and the occurrence of the word in each section

        """
        self.occurrenceMap = {}
        for section in paper.getSections():
            sectionIndex = section.getSectionIndex()
            sectionText = section.getText()
            wordList = word_tokenize(sectionText)
            for wordForm in wordList:
                word = section.getPaper().getWordFromVocabulary(wordForm)
                if word is not None and word.isCandidateFeature():
                    if word.getLemma() in self.occurrenceMap:
                        # If the word exist in the vocabulary and has occurred in the under-processing section
                        # we increase its occurrence in this section
                        if sectionIndex in self.occurrenceMap[word.getLemma()].keys():
                            self.occurrenceMap[word.getLemma()][sectionIndex] += 1
                        # Or we add it to our vocabulary set with its first occurrence in the corresponding section
                        else:
                            self.occurrenceMap[word.getLemma()][sectionIndex] = 1
                    else:
                        self.occurrenceMap[word.getLemma()] = {sectionIndex: 1}
        # Creating an int list of sections
        self.sectionsArray = range(0, paper.getSectionsNum())
        # Converting the dictionary of occurrence to an array. Adding the dic info to array of zeros
        w, h = len(self.sectionsArray), len(self.occurrenceMap.keys())
        self.occurrenceArray = [[0 for x in range(h)] for y in range(w)]
        for word in self.occurrenceMap.keys():
            wordIndex = self.occurrenceMap.keys().index(word)
            for sectionIndex in self.occurrenceMap[word].keys():
                self.occurrenceArray[sectionIndex][wordIndex] = self.occurrenceMap[word][sectionIndex]
