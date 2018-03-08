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
import copy
import random
import json

'''
Cosine scoring function for the unknown document and the corpus index
'''
def cosineSimilarity(vector1, vector2):
    similarity = 0
    mag1 = 0
    mag2 = 0
    for i in range(len(vector1)):
        similarity += float(vector1[i])*float(vector2[i])
        mag1 += vector1[i]**2
        mag2 += vector2[i]**2

    return similarity / (sqrt(mag1) * sqrt(mag2))

'''
Given a list of scores with relation to centers, output the clusters
'''
def cluster(inv_index, centroids, vectors):
    clusters = {}
    # while(1):
    oldClusters = copy.deepcopy(clusters)
    count = 0
    while(1):
    # clustering
        for doc in inv_index[3].keys():
            m = [-1, -1] # [centroid, docid]
            mVal = -1
            for centroid in centroids:
                val = cosineSimilarity(vectors[centroid], vectors[doc]) 
                if mVal < val:
                    m = [centroid, doc]
                    mVal = val
            if m[0] not in clusters:
                clusters[m[0]] = set()
            clusters[m[0]].add(m[1])

        if clusters == oldClusters:
            return clusters

        # refinement
        for cluster in clusters:
            Wk = clusters[cluster]
            for i in range(len(vectors[cluster])):
                s = 0
                for x in Wk:
                    s += vectors[x][i]
                vectors[cluster][i] = (1 / len(Wk)) * s

        oldClusters = copy.deepcopy(clusters)

        count += 1

'''
generate vectors for docs 
'''
def gen_vectors(inv_index):
    vectors = {}
    for doc in inv_index[3].keys():
        vector = []
        for term in inv_index[0]:
            if int(doc) in [x[0] for x in inv_index[0][term]['postings']]:
                i = [x[0] for x in inv_index[0][term]['postings']].index(int(doc))
                vector.append(inv_index[0][term]['postings'][i][1]['tf-idf'])
            else:
                vector.append(0)
        vectors[doc] = vector

    return vectors

if __name__ == "__main__":
    INDEX_FILENAME = "index.json"

    # ensure proper calling format
    if len(argv) < 3:
        raise SyntaxError("Expected usage ./k_means_clusterer.py [index dir] [k] [optional id_1 id_2 ... id_k]")

    directory = argv[1]

    try:
        index_file = open(directory + "/" + INDEX_FILENAME)
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")

    inv_index = json.loads([w for w in index_file][0])

    k = int(argv[2])
    if len(argv) >= 4:
        ids = argv[3:]
        if len(ids) != k:
            raise SyntaxError("Expected k ids")
    else:
        ids = []
        docids = list(inv_index[3].keys())
        for i in range(min(k, len(docids))):
            num = random.randint(0, len(docids) - 1)
            while docids[num] in ids:
                num = random.randint(0, len(docids) - 1)
            ids.append(docids[num])

    for i, doc in enumerate(ids):
        if doc not in inv_index[3]:
            raise SyntaxError("Please make sure all documents are in the corpus")

    result = cluster(inv_index, ids, gen_vectors(inv_index))

    for i, cluster in enumerate(result):
        print(i + 1,",".join(sorted(result[cluster], key=lambda x: int(x))))

#---------------UNIT TESTS-----------------

def test_cosineSimilarity():
    assert(cosineSimilarity([0.72679,0.53393,0.17823,0.14599,0.64471,0.62923,0.26436,0.56584,0.28116,0.79111], [0.62699,0.19872,0.88932,0.44461,0.49034,0.30221,0.00470,0.00470,0.74217,0.16658]) == 1.6358450099)
    assert(cosineSimilarity([0,0,0,0],[0,0,0,0]) == 0.0)
    assert(cosineSimilarity([1,1,1,1],[1,1,1,1]) == 4.0)
    assert(cosineSimilarity([],[]) == 0)

def test_gen_vectors():
    inv_index = [{"earth": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [0]}]]}, "futur": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [1]}]]}, "ha": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [2, 43]}]]}, "been": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [3]}]]}, "riddl": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [4]}]]}, "by": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [5]}]]}, "disast": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [6]}]]}, "famin": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [7]}]]}, "and": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [8]}]]}, "drought": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [9]}]]}, "there": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [10]}]]}, "is": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [11]}]]}, "onli": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [12]}]]}, "one": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [13]}]]}, "way": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [14]}]]}, "to": {"df": 1, "postings": [[0, {"tf": 3, "tf-idf": 0.0, "pos": [15, 38, 54]}]]}, "ensur": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [16]}]]}, "mankind": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [17]}]]}, "surviv": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [18]}]]}, "interstellar": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [19]}]]}, "travel": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [20]}]]}, "a": {"df": 1, "postings": [[0, {"tf": 3, "tf-idf": 0.0, "pos": [21, 34, 46]}]]}, "newli": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [22]}]]}, "discov": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [23]}]]}, "wormhol": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [24]}]]}, "in": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [25]}]]}, "the": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [26, 51]}]]}, "far": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [27]}]]}, "reach": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [28]}]]}, "of": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [29, 36]}]]}, "our": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [30]}]]}, "solar": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [31]}]]}, "system": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [32]}]]}, "allow": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [33]}]]}, "team": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [35]}]]}, "astronaut": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [37]}]]}, "go": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [39]}]]}, "where": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [40]}]]}, "no": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [41]}]]}, "man": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [42]}]]}, "gone": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [44]}]]}, "befor": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [45]}]]}, "planet": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [47]}]]}, "that": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [48]}]]}, "may": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [49]}]]}, "have": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [50]}]]}, "right": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [52]}]]}, "environ": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [53]}]]}, "sustain": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [55]}]]}, "human": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [56]}]]}, "life": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [57]}]]}}, 1, {"0": 58}, {"0": None}]
    assert(gen_vectors(inv_index) == {'0': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})


def test_cluster():
    inv_index = [{"earth": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [0]}]]}, "futur": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [1]}]]}, "ha": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [2, 43]}]]}, "been": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [3]}]]}, "riddl": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [4]}]]}, "by": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [5]}]]}, "disast": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [6]}]]}, "famin": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [7]}]]}, "and": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [8]}]]}, "drought": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [9]}]]}, "there": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [10]}]]}, "is": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [11]}]]}, "onli": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [12]}]]}, "one": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [13]}]]}, "way": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [14]}]]}, "to": {"df": 1, "postings": [[0, {"tf": 3, "tf-idf": 0.0, "pos": [15, 38, 54]}]]}, "ensur": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [16]}]]}, "mankind": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [17]}]]}, "surviv": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [18]}]]}, "interstellar": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [19]}]]}, "travel": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [20]}]]}, "a": {"df": 1, "postings": [[0, {"tf": 3, "tf-idf": 0.0, "pos": [21, 34, 46]}]]}, "newli": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [22]}]]}, "discov": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [23]}]]}, "wormhol": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [24]}]]}, "in": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [25]}]]}, "the": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [26, 51]}]]}, "far": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [27]}]]}, "reach": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [28]}]]}, "of": {"df": 1, "postings": [[0, {"tf": 2, "tf-idf": 0.0, "pos": [29, 36]}]]}, "our": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [30]}]]}, "solar": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [31]}]]}, "system": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [32]}]]}, "allow": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [33]}]]}, "team": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [35]}]]}, "astronaut": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [37]}]]}, "go": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [39]}]]}, "where": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [40]}]]}, "no": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [41]}]]}, "man": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [42]}]]}, "gone": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [44]}]]}, "befor": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [45]}]]}, "planet": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [47]}]]}, "that": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [48]}]]}, "may": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [49]}]]}, "have": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [50]}]]}, "right": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [52]}]]}, "environ": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [53]}]]}, "sustain": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [55]}]]}, "human": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [56]}]]}, "life": {"df": 1, "postings": [[0, {"tf": 1, "tf-idf": 0.0, "pos": [57]}]]}}, 1, {"0": 58}, {"0": None}]
    assert(cluster(inv_index, ['0'], gen_vectors(inv_index)) == {'0': {'0'}})
