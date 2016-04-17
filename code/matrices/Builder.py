from pycorpus import loader
from scipy.sparse import csr_matrix
class MatricesBuilder:
    
    @staticmethod
    def buildMatrices(xmlFile):
        docs = [["hello", "world", "hello"], ["goodbye", "cruel", "world"]]
        document = []
        for section in xmlFile.sections :
            sectionArr = []
            for i in xrange(0,len(section)):  
                sentence =  section[i].split(' ')
                sectionArr.append(sentence)
            document.append(sectionArr)

        indptr = [0]
        indices = []
        data = []
        vocabulary = {}
        #for section in document:
        for sentence in document[0]:
            for term in sentence:
                index = vocabulary.setdefault(term, len(vocabulary))
                indices.append(index)
                data.append(1)
            indptr.append(len(indices))
        
        print csr_matrix((data, indices, indptr), dtype=int).toarray()
        return []
    
    @staticmethod
    def getClustersList(XMLFile):
        return []
    
    @staticmethod
    def getLabelColumn(XMLFile):
        return []