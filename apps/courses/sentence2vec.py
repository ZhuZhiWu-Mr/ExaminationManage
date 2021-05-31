import numpy as np
from sklearn.decomposition import PCA
from typing import List

# see spacy_sentence2vec.py for an example usage with real language inputs


# an embedding word with associated vector
class Word:
    def __init__(self, text, vector):
        self.text = text
        self.vector = vector

    def __str__(self):
        return self.text + ' : ' + str(self.vector)

    def __repr__(self):
        return self.__str__()


# a sentence, a list of words
class Sentence:
    def __init__(self, word_list):
        self.word_list = word_list

    # return the length of a sentence
    def len(self) -> int:
        return len(self.word_list)

    def __str__(self):
        word_str_list = [word.text for word in self.word_list]
        return ' '.join(word_str_list)

    def __repr__(self):
        return self.__str__()


# todo: get a proper word frequency for a word in a document set
# or perhaps just a typical frequency for a word from Google's n-grams
# def get_word_frequency(word_text):
#     return 0.0001  # set to a low occurring frequency - probably not unrealistic for most words, improves vector values

def get_word_frequency(word_text, looktable):
    if word_text in looktable:
        return float(looktable[word_text])
    else:
        return 1

# A SIMPLE BUT TOUGH TO BEAT BASELINE FOR SENTENCE EMBEDDINGS
# Sanjeev Arora, Yingyu Liang, Tengyu Ma
# Princeton University
# convert a list of sentence with word2vec items into a set of sentence vectors
def sentence_to_vec(sentence_list: List[Sentence],embedding_size: int, mydict, a: float=0.00001):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            a_value = a / (a + get_word_frequency(word.text, mydict))  # smooth inverse frequency, SIF
            try:
                # word_list.append(Word(word, model[word.lower()]))
                vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector
            except KeyError:
                vs = np.add(vs, np.multiply(a_value, np.random.uniform(-1, 1, embedding_size)))  # vs += sif * word_vector
                continue

            # vs = np.add(vs, np.multiply(a_value,model[word] ))  # vs += sif * word_vector

        vs = np.divide(vs, sentence_length)  # weighted average
        # vs = vs * 0.8 + 0.2 *len()
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u,vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs
