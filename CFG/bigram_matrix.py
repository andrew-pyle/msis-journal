"""
Issues:
    1. Does too much: no tokenization, just create the matrix
"""

# from stanfordcorenlp import StanfordCoreNLP
from nltk import word_tokenize
import numpy as np
import re

class Corpus(object):
    """
    Constructs the object to control state for rating text samples.
    TODO: class methods instead of independent functions
    """

    def __init__(self, text):
        self.text = text
        self.tokens = tokenize_text(self.text)
        self.unique_tokens = get_token_indices(self.tokens)
        self.markov_matrix = generate_markov_transitions(self.tokens,                                                            self.unique_tokens)

def tokenize_text(text):
    """
    wrapper to tokenize text. Possibly change methods.

    params:
        text (str): text to tokenize.

    returns:
        (list): tokenized text.
    """
    regex = re.compile(r'''https?:\/\/\S*|[^\u0000-\u0fff]|[\w\@\#\$\%\^\&\*\(\)\{\}\_\-\+\=\'\"]+|[!?.,;:]''')
    tokens = regex.findall(text)

    # tokens = word_tokenize(text)

    return tokens

def get_token_indices(tokens):
    """
    Generates list of unique tokens which can serve as input to and indices for
    generate_markov_transitions().

    params:
        tokens (list): Tokenized text.

    returns:
        (list): Unique tokens.
    """

    # Create specified order for matrix indices
    token_index_lookup = []
    for token in tokens:
        if token not in token_index_lookup:
            token_index_lookup.append(token)

    # print(token_index_lookup)  # debug

    return token_index_lookup


def generate_markov_transitions(tokens, token_list):
    """

    params:
        tokens (list): tokenized text.
        token_list (list): unique tokens (in alphabetical order?).

    returns:
        (numpy matrix): token_list by token_list matrix. Can be queried based
            on token_list

    Only for Bigrams

    Based on StackOverflow answer by John Coleman
        https://stackoverflow.com/questions/46657221/generating-markov-
        transition-matrix-in-python?rq=1
    """

    # Generate frequency matrix
    freq_matrix = np.zeros((len(token_list), len(token_list)))

    for (i,j) in zip(tokens, tokens[1:]):
        freq_matrix[token_list.index(i),
                    token_list.index(j)] += 1

    # print(freq_matrix)  # debug

    # Create probability matrix from frequency matrix
    prob_matrix = np.zeros((len(token_list), len(token_list)))

    for row_num in range(len(freq_matrix)):
        s = sum(freq_matrix[row_num])
        if s > 0:  # avoid divide by zero
            prob_matrix[row_num] = freq_matrix[row_num,:] / s

    # print(prob_matrix)  # debug

    return prob_matrix

def rate_sentence(sentence, corpus):
    """
    Calculates the sum of the bigram transition probabilities of a sentence according to a corpus.

    params:
        sentence (str): Sample of text to score.
        corpus (Corpus): Holds bigram transition probabilities

    returns:
        (float): Sum of bigram transition probabilities
    """
    tokens = word_tokenize(sentence)

    bigrams = zip(tokens, tokens[1:])
    score = 0

    for bigram in bigrams:
        try:
            idx0 = corpus.unique_tokens.index(bigram[0])
            idx1 = corpus.unique_tokens.index(bigram[1])

            prob = corpus.markov_matrix[idx0, idx1]
            score += prob
        except:
            pass

    return score

# Test Harness
if __name__ == '__main__':

    # text = '''The top Leadership and Investigators of the FBI and the Justice
    # Department have politicized the sacred investigative process in favor of
    # Democrats and against Republicans - something which would have been
    # unthinkable just a short time ago? Rank & File are great people!
    # Republicans are now leading the Generic Poll, perhaps because of
    # the popular Tax Cuts which the Dems want to take away. Actually, they want
    # to raise you taxes, substantially. Also, they want to do nothing on DACA,
    # R’s want to fix! The U.S. economy is looking very good, in my opinion, even
    # better than anticipated. Companies are pouring back into our country,
    # reversing the long term trend of leaving. The unemployment numbers are
    # look'''

    text = '''the quick brown fox jumps over the quick black dog.'''

    # tokens = tokenize_text(text)
    # index_lookup = get_token_indices(tokens)
    # print(index_lookup)
    # markov_trans = generate_markov_transitions(tokens, index_lookup)

    # print(markov_trans)

    # the_index = index_lookup.index('the')
    # black_index = index_lookup.index('black')
    # print(markov_trans[the_index, black_index])

    # and_index = index_lookup.index('and')
    # the_index = index_lookup.index('the')
    # against_index = index_lookup.index('the')

    # sacred_index = index_lookup.index('sacred')
    # investigative_index = index_lookup.index('investigative')

    # are_index = index_lookup.index('are')
    # great_index = index_lookup.index('great')

    # print(markov_trans[and_index, against_index])
    # print(markov_trans[and_index, the_index])
    # print(markov_trans[sacred_index, investigative_index])
    # print(markov_trans[and_index, sacred_index])

    # print(markov_trans[are_index, great_index])

    corpus = Corpus(text)
    sent = 'The top Leadership of the FBI is looking very good'

    print(rate_sentence(sent, corpus))
