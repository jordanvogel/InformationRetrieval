#!/usr/local/bin/python3
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
from os import listdir
from sys import argv
from math import ceil
from math import log10
import json

REMOVE_STOPWORDS = False

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
    doclen = {}
    for f in sorted(listdir(directory), key=lambda x: int(x.split("_")[1])):
        DOC_COUNT += 1
        docid = int(f.split("_")[1])
        doc = open(directory + "/" +f, "r")

        docText = [w.lower() for w in doc][0].translate(punct_translator)
        docText = [stemmer.stem(w.lower()) for w in word_tokenize(docText)]

        # if you don't like data structures turn away

        pos = 0
        for word in docText:
            if word in stopwords_set and REMOVE_STOPWORDS:
                pos += 1
                continue
            if word not in index:
                index[word] = {'df':1, 'postings':[(docid,{'tf':1, 'tf-idf':0, 'pos':[pos]})]}
            else:
                doc_index = bin_search(docid, index[word]['postings'])
                # docid in posting list
                if doc_index[0]:
                    index[word]['postings'][doc_index[1]][1]['pos'].append(pos)
                    index[word]['postings'][doc_index[1]][1]['tf'] += 1
                # docid not in posting list
                else:
                    index[word]['postings'].insert(doc_index[1], (docid, {'tf':1,'tf-idf':0, 'pos':[pos]}))
                    index[word]['df'] += 1
            pos += 1

        doclen[docid] = pos

    # Now calculate the tf-idf and update it for every entry in the index
    # This doesnt have a unit test as it is just a math formula, and we would just be testing for order of operations.
    for term in index.keys():
        for docid_index in range(len(index[term]['postings'])):
            index[term]['postings'][docid_index][1]['tf-idf'] = float((1 + log10(index[term]['postings'][docid_index][1]['tf'])) * log10(DOC_COUNT/int(index[term]['df'])))

    return (index, DOC_COUNT, doclen)

if __name__ == "__main__":
    INDEX_FILENAME = "index.json"

    # ensure proper calling format
    if len(argv) != 2:
        raise SyntaxError("Expected usage ./create_index.py [dir]")

    directory = argv[1]
    
    index = generate_posting_list(directory)

    index_file = open(INDEX_FILENAME, 'w')
    index_file.write(json.dumps(index, indent=4))

#---------------UNIT TESTS-----------------

#Tests if our binary search for inserting into the index is working properly
def test_bin_search():
    l = [(1, {}), (3, {}), (4, {}), (6, {}), (8, {}), (9, {}), (10, {}), (11, {}), (13, {}), (15, {}), (19, {}), (35, {}), (56, {}), (192, {}), (500, {})]
    assert(bin_search(1, l) == (True, 0))
    assert(bin_search(500, l) == (True, 14))
    assert(bin_search(10, l) == (True, 6))
    assert(bin_search(12, l) == (False, 8))

    l = [(1, {})]
    assert(bin_search(1, l) == (True, 0))
    assert(bin_search(2, l) == (False, 1))
    assert(bin_search(0, l) == (False, 0))

    l = []
    assert(bin_search(1, l) == (False, 0))
	
#Testing if our lambda function to sort the docs in the corpus works properly
def test_lambda_sort():
    l = ["doc_132_yep", "doc_6_Nope", "doc_130_helpme", "doc_1_plz"]
    f = sorted(l, key = lambda x: int(x.split("_")[1]))
    assert(f == ["doc_1_plz", "doc_6_Nope", "doc_130_helpme", "doc_132_yep"])
    
#Testing translator for the removal of punctuation
def test_punct_remove():
    punct_translator = str.maketrans('', '', punctuation)
    sentence = "Hello. My name, is! not 'this': I don't think; at least.!?"
    ts = sentence.translate(punct_translator)
    assert(ts == "Hello My name is not this I dont think at least")
