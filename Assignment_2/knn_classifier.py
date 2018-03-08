#!/usr/local/bin/python3
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
from os import listdir
from sys import argv
from math import ceil
from math import log10
from math import sqrt
import json

'''
binary search to find index of docid in list
returns tuple (True/False, index)
'''
def bin_search(docid, lst):
    lo = 0
    hi = len(lst) - 1
    while(lo <= hi):
        mid = ceil((hi + lo) / 2)
        if (lst[mid][0] > docid):
            hi = mid - 1
        elif (lst[mid][0] < docid):
            lo = mid + 1
        else:
            return (True, mid)
    mid = ceil((hi + lo) / 2)
    return (False, mid)

'''
Generates the posting lists with df and tf for each word with stemming and tokenization
'''
def generate_posting_list(directory):
    DOC_COUNT = 0
    # translator for removing punctuation
    punct_translator = str.maketrans('', '', punctuation)

    # store stopwords as a set for fast lookup
    stopwords_set = set(stopwords.words('english'))

    # using porter stemmer
    stemmer = PorterStemmer()
    index = {}
    
    for f in sorted(listdir(directory), key=lambda x: int(x.split(".")[0])):
        doc = open(directory + "/" +f, "r")

        docText = [w.lower() for w in doc][0].translate(punct_translator)
        docText = [stemmer.stem(w.lower()) for w in word_tokenize(docText)]

        # Much simpler index for the single query document. DF always 1, so not stored at all

        pos = 0
        for word in docText:
            if word in stopwords_set:
                pos += 1
                continue
            if word not in index:
                # first time seeing word
                index[word] = {'tf':1, 'tf-idf':0, 'pos':[pos]}
            else:
                # already in the index
                index[word]['pos'].append(pos)
                index[word]['tf'] += 1
            pos += 1

        doclen = pos

        # Now calculate the tf-idf and update it for every entry in the index

        # Origional tf-idf computation
        for term in index.keys():
            index[term]['tf-idf'] = float(1 + log10(index[term]['tf']))
        
    return (index, doclen)

'''
Cosine scoring function for the unknown document and the corpus index
'''
def cosineScore(index, query):
        #uses precomputed value that is the size of the document corpus, made on creation
        CORPUS_SIZE = index[1]
        doc_length_list = index[2]
        Scores = {}
        for term in query[0]:
            w_t_q = query[0][term]['tf-idf']
            if term in index[0].keys():
                for i, doc in enumerate(index[0][term]['postings']):
                    if doc[0] in Scores:
                        Scores[doc[0]][0] += index[0][term]['postings'][i][1]['tf-idf'] * w_t_q
                    else:
                        Scores[doc[0]] = [index[0][term]['postings'][i][1]['tf-idf'] * w_t_q , doc[2]]
            
        answer = []
        for doc in Scores:
            answer.append((doc, Scores[doc][0] / doc_length_list[str(doc)], Scores[doc][1]))
        return answer

'''
Function to print out the list of ranked results in decreasing order of 
relevence.
'''
def rank_results(scores, k):
    #using a lambda to sort through the scores by the second element
    sort_scores = [s for s in sorted(scores, key = lambda x: x[1], reverse = True)]
    # create a dict of category, with the values being the count
    answer = {}
    for i in range(0, min(k, len(sort_scores))):
        if sort_scores[i][2] in answer.keys():
            answer[sort_scores[i][2]] += 1
        else:
            answer[sort_scores[i][2]] = 1

    # this just takes all the items in the dict and returns a descending sorted list of keys, sorted by values
    #answer = answer.items()
    maxV = max(answer.values())

    return ' '.join([x if answer[x] == maxV else '' for x in answer])

if __name__ == "__main__":
    INDEX_FILENAME = "class_index.json"

    # ensure proper calling format
    if len(argv) != 4:
        raise SyntaxError("Expected usage ./knn_classifier [index dir] [k] [q]")

    directory = argv[1]
    k = int(argv[2])
    unseen = argv[3]
    
    unseen_index = generate_posting_list(unseen)

    try:
        index_file = open(directory + "/" + INDEX_FILENAME, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")

    index = json.loads([w for w in index_file][0])

    print(rank_results(cosineScore(index, unseen_index), k))
    


#---------------UNIT TESTS-----------------

#Testing translator for the removal of punctuation
def test_punct_remove():
    punct_translator = str.maketrans('', '', punctuation)
    sentence = "Hello. My name, is! not 'this': I don't think; at least.!?"
    ts = sentence.translate(punct_translator)
    assert(ts == "Hello My name is not this I dont think at least")

def test_cosineScore():
    #testing on a small sample database 
    index = [{"word": {"df": 1, "postings": [[4, {"tf": 1, "pos": [20], "tf-idf": 0.6020599913279624}]]}, "chop": {"df": 1, "postings": [[4, {"tf": 1, "pos": [14], "tf-idf": 0.6020599913279624}]]}, "of": {"df": 2, "postings": [[3, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [4, {"tf": 1, "pos": [18], "tf-idf": 0.3010299956639812}]]}, "never": {"df": 2, "postings": [[1, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}]]}, "a": {"df": 3, "postings": [[1, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [2, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [4, {"tf": 2, "pos": [11, 19], "tf-idf": 0.16254904394775974}]]}, "but": {"df": 1, "postings": [[4, {"tf": 1, "pos": [7], "tf-idf": 0.6020599913279624}]]}, "recal": {"df": 1, "postings": [[2, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "process": {"df": 1, "postings": [[4, {"tf": 1, "pos": [10], "tf-idf": 0.6020599913279624}]]}, "size": {"df": 1, "postings": [[3, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "at": {"df": 1, "postings": [[4, {"tf": 1, "pos": [4], "tf-idf": 0.6020599913279624}]]}, "end": {"df": 1, "postings": [[4, {"tf": 1, "pos": [17], "tf-idf": 0.6020599913279624}]]}, "in": {"df": 2, "postings": [[1, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}]]}, "stem": {"df": 4, "postings": [[1, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [2, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [3, {"tf": 1, "pos": [0], "tf-idf": 0.0}], [4, {"tf": 2, "pos": [0, 13], "tf-idf": 0.0}]]}, "be": {"df": 1, "postings": [[4, {"tf": 1, "pos": [2], "tf-idf": 0.6020599913279624}]]}, "not": {"df": 1, "postings": [[4, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "should": {"df": 1, "postings": [[4, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "queri": {"df": 1, "postings": [[4, {"tf": 1, "pos": [12], "tf-idf": 0.6020599913279624}]]}, "time": {"df": 1, "postings": [[4, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}, "lower": {"df": 2, "postings": [[1, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}]]}, "retriev": {"df": 2, "postings": [[1, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}]]}, "increas": {"df": 1, "postings": [[3, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "off": {"df": 1, "postings": [[4, {"tf": 1, "pos": [15], "tf-idf": 0.6020599913279624}]]}, "index": {"df": 1, "postings": [[4, {"tf": 1, "pos": [5], "tf-idf": 0.6020599913279624}]]}, "system": {"df": 2, "postings": [[1, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}]]}, "the": {"df": 2, "postings": [[3, {"tf": 2, "pos": [2, 5], "tf-idf": 0.39164905395343774}], [4, {"tf": 1, "pos": [16], "tf-idf": 0.3010299956639812}]]}, "boolean": {"df": 2, "postings": [[1, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}]]}, "invok": {"df": 1, "postings": [[4, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "while": {"df": 1, "postings": [[4, {"tf": 1, "pos": [9], "tf-idf": 0.6020599913279624}]]}, "precis": {"df": 1, "postings": [[1, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "vocabulari": {"df": 1, "postings": [[3, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}}, 4, {"1": 9, "2": 9, "3": 7, "4": 21}]

    score = cosineScore(index, ["word"]) 
    assert(score[0] == (4, 0.03974439862065926))

    score2 = cosineScore(index, ["chop", "word"])
    assert(score2 == [(4, 0.07948879724131852)])

def test_rank_result():
    # small snippet of a database taken from the actual data
    results = [(0, 0.7506997370065573, 'Drama'), (1, 0.019666539584895015, 'Drama'), (2, 0.015404422993538102, 'Drama'), (3, 0.02653929608841955, 'Drama'), (4, 0.00803413798087378, 'Drama'), (5, 0.0057425486943661844, 'Drama'), (14, 0.016280937903468174, 'Animation'), (15, 0.02343622367933958, 'Animation'), (16, 0.013313202488644661, 'Animation'), (17, 0.019591609254030213, 'Animation')]

    assert(rank_results(results, 5).strip() == 'Drama')

    assert(rank_results(results, 1).strip() == 'Drama')
