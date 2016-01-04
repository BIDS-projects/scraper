import numpy as np
import lda


def createDocTermMat(dataset):
    """
    Transform the dataset from json to a document-term matrix.
    
    A document-term matrix is a matrix of documents vs terms present in the collection of documents. 
    The entries denote the frequency of a term in a given document.
    
    Returns a triple of the data matrix, list of terms present in the corpus, and document titles.
    
    Need to find a way to cleanly distinguish between documents, i.e. need labels. Needs to be unique. 
    Note that the identifiers depend on what we choose as our definition for documents. For now this is all the text in a web directory. Future studies: research paper, papers of researchers, summary of institution, institutional research papers.
    MISSING IMPLEMENTATION
    """
    pass

class LDA:
    def __init__(self, number_topics):
        self.model = lda.LDA(n_topics=number_topics, n_iter=1000, alpha = .05, eta = .005)
    
    def fit(self, dataset):
        [dataMatrix, terms, documents] = createDocTermMat(dataset)
        self.terms = terms
        self.documents = documents
        self.model.fit(dataMatrix)

    def printTopics(self, n_words):
    """
    Prints the top n_words for each topic.

    Things to think about: A way to visualize the distribution of these words in each topic.
    """
        for i, top_dist in enumerate(self.model.topic_word_):
            topic_words = np.array(terms)[np.argsort(topic_dist)][:-(n_words+1)]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))


    def printDocTopic(self):
    """
    Prints the document in order indicates which topic it is most likely under.

    Possible additions: Add the top three most likely topics. Indicate the likelihood.
    Things to think about: Look for documents that may be allocated to different topics. i.e. look at the likelihood and if it surpasses a certain threshold for more than one topic indicate it. This could lead to further study.
    """
        doc_topic = self.model.doc_topic_
        for i in range(len(self.documents)):
            print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
