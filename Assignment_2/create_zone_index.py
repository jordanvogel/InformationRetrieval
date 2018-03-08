#!/usr/local/bin/python3
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from os import listdir
from sys import argv
from math import ceil
from math import log10
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

    # using porter stemmer
    stemmer = PorterStemmer()
    index = {}
    tit_index = {}
    for f in sorted(listdir(directory), key=lambda x: int(x.split(".")[0])):
        docid = int(f.split(".")[0])
        doc = open(directory + "/" +f, "r")

        title_text = [stemmer.stem(w) for w in word_tokenize(doc.readline().translate(punct_translator))]

        docText = [w.lower() for w in doc][0].translate(punct_translator)
        docText = [stemmer.stem(w) for w in word_tokenize(docText)]

        pos = 0
        for word in title_text:
            if word not in tit_index:
                tit_index[word] = {docid:[pos]}
            else:
                if docid in tit_index[word]:
                    tit_index[word][docid].append(pos)
                else:
                    tit_index[word][docid] = [pos]
            pos += 1
        
        # if you don't like data structures turn away
        pos = 0
        for word in docText:
            if word not in index:
                index[word] = {docid:[pos]}
            else:
                # docid in posting list
                if docid in index[word]:
                    index[word][docid].append(pos)
                # docid not in posting list
                else:
                    index[word][docid] = [pos]
            pos += 1

    return (index, tit_index) 

if __name__ == "__main__":
    INDEX_FILENAME = "zone_index.json"

    # ensure proper calling format
    if len(argv) != 3:
        raise SyntaxError("Expected usage ./create_index.py [document dir] [index dir]")

    doc_dir= argv[1]
    index_dir= argv[2]
    
    index = generate_posting_list(doc_dir)

    index_file = open(INDEX_FILENAME, 'w')
    index_file.write(json.dumps(index))

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
