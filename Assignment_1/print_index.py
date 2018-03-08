#!/usr/local/bin/python3
from sys import argv
from difflib import Differ
import json

'''
iterates through index and builds string
to fit the required format
Preconditions:
    index should fit the index format defined in create_index.py
'''
def index_to_string(index):
    out = ""
    for term in index:
        out += term + "\t"
        for doc in index[term]['postings']:
            # append docid
            out += str(doc[0]) + ":"
            for pos in doc[1]['pos']:
                # append positions, with proper field separators
                out += str(pos)
                out += "," if pos != doc[1]['pos'][-1] else ";" if doc[0] != index[term]['postings'][-1][0] else "\n"
    return out

if __name__ == "__main__":
    INDEX_FILENAME = "index.json"

    # ensure proper calling format
    if len(argv) != 2:
        raise SyntaxError("Expected usage ./print_index.py [dir]")

    directory = argv[1]

    # open file if it exists
    try:
        index_file = open(directory + "/" + INDEX_FILENAME, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")

    index = json.loads([w for w in index_file][0])[0]

    print(index_to_string(index), end="")

#---------------UNIT TESTS-----------------
def test_print_index():
    # test relatively large index
    index = { "word_1": { "df": 2, "postings": [ [ 1, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 0 ] } ], [ 2, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 0 ] } ] ] }, "word_2": { "df": 2, "postings": [ [ 1, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 1 ] } ], [ 2, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 1 ] } ] ] }, "word_3": { "df": 2, "postings": [ [ 1, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 2 ] } ], [ 2, { "tf": 1, "tf-idf": 0.3010299956639812, "pos": [ 2 ] } ] ] }}
    expected = """word_1\t1:0;2:0\nword_2\t1:1;2:1\nword_3\t1:2;2:2\n"""
    assert(expected == index_to_string(index))

    # test with index with one element
    index = { "word_1": { "df": 1, "postings": [ [ 1, {"tf": 1, "tf-idf": 1.00, "pos": [ 0 ] } ] ] }}
    expected = """word_1\t1:0\n"""
    assert(expected == index_to_string(index))

    # test empty index
    index = {}
    expected = ""
    assert(expected == index_to_string(index))
