#!/usr/local/bin/python3
from sys import argv
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import math
import json

punct_translator = str.maketrans('', '', punctuation)
stemmer = PorterStemmer()

'''
Function to print out the list of ranked results in decreasing order of 
relevence.
'''
def rank_results(scores, k, flag):
    #using a lambda to sort through the scores by the second element
    sort_scores = [s for s in sorted(scores, key = lambda x: x[1])]
    #checking if flag is wanted
    if flag == 'y':
        answer = []
        for i in range(0, min(k, len(sort_scores))):
            #did funny string conversion as having a list ints and then adding (NUM) after it was harder than i wanted it to be
            answer.append(str(sort_scores[i][0]) + "(" + str(sort_scores[i][1]) + ")")
    elif flag == 'n':
        answer = []
        for i in range(0, min(k, len(sort_scores))):
            #just prints the docs, without the scores
            answer.append(sort_scores[i][0])
    return answer


'''
Function to compute the cosine score for the given query
'''
#Lots of this was modeled/used from the starter code given to us
def cosineScore(index, query):
    #uses precomputed value that is the size of the document corpus, made on creation
    CORPUS_SIZE = index[1]
    doc_length_list = index[2]
    Scores = {}
    for term in query:
        w_t_q = math.log( CORPUS_SIZE / index[0][term]['df'])
        for i, doc in enumerate(index[0][term]['postings']):
            if doc[0] in Scores:
                Scores[doc[0]] += index[0][term]['postings'][i][1]['tf-idf'] * w_t_q
            else:
                Scores[doc[0]] = index[0][term]['postings'][i][1]['tf-idf'] * w_t_q
    answer = []
    for doc in Scores:
        answer.append((doc, Scores[doc] / doc_length_list[str(doc)]))
    return answer



if __name__ == "__main__":
    INDEX_FILENAME = "index.json"

    if len(argv) < 5:
        raise SyntaxError("Expected usage ./vs_query.py [index location] [k] [scores] [term_1] [term_2] ... [term_n]")

    directory = argv[1]
    k = int(argv[2])
    scores = argv[3].lower()
    terms = argv[4:]
    try:
        index_file = open(directory + "/" + INDEX_FILENAME , 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")

    index = json.loads([w for w in index_file][0])
    format_terms = []
    for i in range(len(terms)):
        terms[i] = terms[i].lower()        
        terms[i] = terms[i].translate(punct_translator)
        terms[i] = stemmer.stem(terms[i].lower())
        format_terms.append(terms[i])

    print(rank_results(cosineScore(index, format_terms), k, scores))


#---------------UNIT TESTS-----------------
def test_cosineScore():
    #testing on a small sample database 
    index = [{"word": {"df": 1, "postings": [[4, {"tf": 1, "pos": [20], "tf-idf": 0.6020599913279624}]]}, "chop": {"df": 1, "postings": [[4, {"tf": 1, "pos": [14], "tf-idf": 0.6020599913279624}]]}, "of": {"df": 2, "postings": [[3, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [4, {"tf": 1, "pos": [18], "tf-idf": 0.3010299956639812}]]}, "never": {"df": 2, "postings": [[1, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}]]}, "a": {"df": 3, "postings": [[1, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [2, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [4, {"tf": 2, "pos": [11, 19], "tf-idf": 0.16254904394775974}]]}, "but": {"df": 1, "postings": [[4, {"tf": 1, "pos": [7], "tf-idf": 0.6020599913279624}]]}, "recal": {"df": 1, "postings": [[2, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "process": {"df": 1, "postings": [[4, {"tf": 1, "pos": [10], "tf-idf": 0.6020599913279624}]]}, "size": {"df": 1, "postings": [[3, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "at": {"df": 1, "postings": [[4, {"tf": 1, "pos": [4], "tf-idf": 0.6020599913279624}]]}, "end": {"df": 1, "postings": [[4, {"tf": 1, "pos": [17], "tf-idf": 0.6020599913279624}]]}, "in": {"df": 2, "postings": [[1, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}]]}, "stem": {"df": 4, "postings": [[1, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [2, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [3, {"tf": 1, "pos": [0], "tf-idf": 0.0}], [4, {"tf": 2, "pos": [0, 13], "tf-idf": 0.0}]]}, "be": {"df": 1, "postings": [[4, {"tf": 1, "pos": [2], "tf-idf": 0.6020599913279624}]]}, "not": {"df": 1, "postings": [[4, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "should": {"df": 1, "postings": [[4, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "queri": {"df": 1, "postings": [[4, {"tf": 1, "pos": [12], "tf-idf": 0.6020599913279624}]]}, "time": {"df": 1, "postings": [[4, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}, "lower": {"df": 2, "postings": [[1, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}]]}, "retriev": {"df": 2, "postings": [[1, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}]]}, "increas": {"df": 1, "postings": [[3, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "off": {"df": 1, "postings": [[4, {"tf": 1, "pos": [15], "tf-idf": 0.6020599913279624}]]}, "index": {"df": 1, "postings": [[4, {"tf": 1, "pos": [5], "tf-idf": 0.6020599913279624}]]}, "system": {"df": 2, "postings": [[1, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}]]}, "the": {"df": 2, "postings": [[3, {"tf": 2, "pos": [2, 5], "tf-idf": 0.39164905395343774}], [4, {"tf": 1, "pos": [16], "tf-idf": 0.3010299956639812}]]}, "boolean": {"df": 2, "postings": [[1, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}]]}, "invok": {"df": 1, "postings": [[4, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "while": {"df": 1, "postings": [[4, {"tf": 1, "pos": [9], "tf-idf": 0.6020599913279624}]]}, "precis": {"df": 1, "postings": [[1, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "vocabulari": {"df": 1, "postings": [[3, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}}, 4, {"1": 9, "2": 9, "3": 7, "4": 21}]

    score = cosineScore(index, ["word"]) 
    assert(score[0] == (4, 0.03974439862065926))

    score2 = cosineScore(index, ["chop", "word"])
    assert(score2 == [(4, 0.07948879724131852)])

def test_rank_results():
    #using the same database, copied over for extra redundancy, to test our ranked retrieval system.
    index = [{"word": {"df": 1, "postings": [[4, {"tf": 1, "pos": [20], "tf-idf": 0.6020599913279624}]]}, "chop": {"df": 1, "postings": [[4, {"tf": 1, "pos": [14], "tf-idf": 0.6020599913279624}]]}, "of": {"df": 2, "postings": [[3, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [4, {"tf": 1, "pos": [18], "tf-idf": 0.3010299956639812}]]}, "never": {"df": 2, "postings": [[1, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [6], "tf-idf": 0.3010299956639812}]]}, "a": {"df": 3, "postings": [[1, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [2, {"tf": 1, "pos": [1], "tf-idf": 0.12493873660829992}], [4, {"tf": 2, "pos": [11, 19], "tf-idf": 0.16254904394775974}]]}, "but": {"df": 1, "postings": [[4, {"tf": 1, "pos": [7], "tf-idf": 0.6020599913279624}]]}, "recal": {"df": 1, "postings": [[2, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "process": {"df": 1, "postings": [[4, {"tf": 1, "pos": [10], "tf-idf": 0.6020599913279624}]]}, "size": {"df": 1, "postings": [[3, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "at": {"df": 1, "postings": [[4, {"tf": 1, "pos": [4], "tf-idf": 0.6020599913279624}]]}, "end": {"df": 1, "postings": [[4, {"tf": 1, "pos": [17], "tf-idf": 0.6020599913279624}]]}, "in": {"df": 2, "postings": [[1, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [0], "tf-idf": 0.3010299956639812}]]}, "stem": {"df": 4, "postings": [[1, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [2, {"tf": 1, "pos": [5], "tf-idf": 0.0}], [3, {"tf": 1, "pos": [0], "tf-idf": 0.0}], [4, {"tf": 2, "pos": [0, 13], "tf-idf": 0.0}]]}, "be": {"df": 1, "postings": [[4, {"tf": 1, "pos": [2], "tf-idf": 0.6020599913279624}]]}, "not": {"df": 1, "postings": [[4, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "should": {"df": 1, "postings": [[4, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "queri": {"df": 1, "postings": [[4, {"tf": 1, "pos": [12], "tf-idf": 0.6020599913279624}]]}, "time": {"df": 1, "postings": [[4, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}, "lower": {"df": 2, "postings": [[1, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [7], "tf-idf": 0.3010299956639812}]]}, "retriev": {"df": 2, "postings": [[1, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [3], "tf-idf": 0.3010299956639812}]]}, "increas": {"df": 1, "postings": [[3, {"tf": 1, "pos": [1], "tf-idf": 0.6020599913279624}]]}, "off": {"df": 1, "postings": [[4, {"tf": 1, "pos": [15], "tf-idf": 0.6020599913279624}]]}, "index": {"df": 1, "postings": [[4, {"tf": 1, "pos": [5], "tf-idf": 0.6020599913279624}]]}, "system": {"df": 2, "postings": [[1, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [4], "tf-idf": 0.3010299956639812}]]}, "the": {"df": 2, "postings": [[3, {"tf": 2, "pos": [2, 5], "tf-idf": 0.39164905395343774}], [4, {"tf": 1, "pos": [16], "tf-idf": 0.3010299956639812}]]}, "boolean": {"df": 2, "postings": [[1, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}], [2, {"tf": 1, "pos": [2], "tf-idf": 0.3010299956639812}]]}, "invok": {"df": 1, "postings": [[4, {"tf": 1, "pos": [3], "tf-idf": 0.6020599913279624}]]}, "while": {"df": 1, "postings": [[4, {"tf": 1, "pos": [9], "tf-idf": 0.6020599913279624}]]}, "precis": {"df": 1, "postings": [[1, {"tf": 1, "pos": [8], "tf-idf": 0.6020599913279624}]]}, "vocabulari": {"df": 1, "postings": [[3, {"tf": 1, "pos": [6], "tf-idf": 0.6020599913279624}]]}}, 4, {"1": 9, "2": 9, "3": 7, "4": 21}]
    
    result = rank_results(cosineScore(index, ["word","chop","never"]), 3, "y")
    assert(result == ['1(0.023184232528717902)', '2(0.023184232528717902)', '4(0.07948879724131852)'])

    result = rank_results(cosineScore(index, ["word", "chop", "never"]), 3, "n")
    assert(result == [1 ,2 ,4])

    result = rank_results(cosineScore(index, ["a"]), 1, "y")
    assert( result == ['4(0.0022267831351403394)'])
