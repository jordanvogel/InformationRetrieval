#!/usr/local/bin/python3
from shlex import split
from sys import argv
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import json
import itertools

'''
Query tree generation for parsing
Comes from our assignment1 code
'''
def query_tree(query):
    operators = {'AND', 'OR'}
    separators = {'(', ')'}
    non_terms = operators.union(separators)
    stemmer = PorterStemmer()

    # ensure query is not empty
    if len(query) == 0:
        raise SyntaxError("Invalid Query")

    # split query into terms etc
    query = split(query.replace('(', ' ( ').replace(')', ' ) ').strip())

    # appply stemming on terms in query
    for index, element in enumerate(query):
        if element not in non_terms:
            # apply stemming on individual terms (also handles sentences)
            query[index] = ' '.join([stemmer.stem(part.lower()) for part in element.split()])

    if len(query) == 1:
        return ("KEYWORD", query[0]) if ' ' not in query[0] else ("PHRASE", query[0])

    # convert the string into a list with eval to make tree building easier
    # While we're at it have a nice little tree Source(http://www.ascii-code.com/ascii-art/holiday-and-events/christmas/trees.php)
    '''
             v
            >X<
             A
            d$b
          .d\$$b.
        .d$i$$\$$b.
           d$$@b
          d\$$$ib
        .d$$$\$$$b
      .d$$@$$$$\$$ib.
          d$$i$$b
         d\$$$$@$b
      .d$@$$\$$$$$@b.
    .d$$$$i$$$\$$$$$$b.
            ###
            ###
            ### mh
    '''
    for index, element in enumerate(query):
        if element == '(':
            query[index] = '['
        elif element == ')':
            query[index] = ']'
        elif element not in non_terms:
            query[index] = '"' + element + '"'
        else:
            query[index] = ',"' + element + '",'

    # adds in parenthesis to account for multiple unbracketed operators
    def rebracket(l):
        while(len(l) > 4):
            l = [l[0:3]] + l[3:]
        return l
    
    # removes redundant parenthesis from query
    def remove_paren(l):
        if type(l) == type(''):
            return l
        if len(l) == 1:
            return remove_paren(l[0])
        if len(l) > 4:
            return remove_paren(rebracket(l))
        try:
            return [remove_paren(l[0]), l[1], remove_paren(l[2])]
        except IndexError:
            raise SyntaxError("Invalid Query")

    # Recursively swap elements to put query into rpn
    def swap(l):
        if len(l) == 1 or type(l) == type(''):
            return l
        return [l[1], swap(l[0]), swap(l[2])]
    
    # Adds KEYWORD delimiter to keywords
    def format_query(q):
        if type(q) == type(''):
            if ' ' in q:
                return ("PHRASE", q)
            return ("KEYWORD", q)
        return [q[0], format_query(q[1]), format_query(q[2])]

    qlist = list(eval("".join(query)))
    qlist = remove_paren(qlist)
    qlist = swap(qlist)
    qlist = format_query(qlist)
    return qlist

'''
Standard intersection formula for posting lists.
'''
def intersect(p1, p2):
    inter_keys = p1.keys() & p2.keys()
    inter_dict = {}

    for key in inter_keys:
        inter_dict[key] = p1[key]

    return inter_dict

'''
Simple union operation for two posting lists
'''
def union(p1, p2):
    union_keys = p1.keys() | p2.keys()
    union_dict = {}

    for key in union_keys:
        union_dict[key] = p1[key] if key in p1 else p2[key]

    return union_dict

'''
Query evaluation taking into account zone scoring
similar to in Assignment 1, but deals with posting lists
as dictionaries

Returns list of documents satisfying query with sb and st
'''
def evaluate_boolean_query(node):
    if node[0] == 'KEYWORD':
        # items in posting list will be docid:[sb, st]
        posting_list = {}
        if node[1] not in index[0] and node[1] not in index[1]:
            return dict()

        # first pass is body, second is title
        for i in range(2):
            # term is in body
            if node[1] in index[i]:
                # for each docid in index[term]
                for item in index[i][node[1]]:
                    if item in posting_list:
                        # set sb to 1
                        posting_list[item][i] = 1
                    else:
                        posting_list[item] =  [i ^ 1, i]

        return posting_list

    elif node[0] == 'PHRASE':
        # items in posting list will be docid:[sb, st]
        posting_list = {}
        for term in node[1].split():
            # if any word is not in the index, then the phrase is not
            if term not in index[0] and term not in index[1]:
                return dict()

        sentence = node[1].split()

        # stores which documents contain the words in the phrase in title
        # and body, docs[0] -> body docs[1] -> title
        docs = [set(), set()]
        # find all documents and titles that contain all words in the sentence
        # start by looking at docs that contain first term
        for i in range(2):
            if sentence[0] not in index[i]:
                continue
            for doc in index[i][sentence[0]]:
                # whether we broke out or got through the sentence
                failed = False
                for term in sentence:
                    if term not in index[i]:
                        failed = True
                        break
                    # generate list of documents that contain term
                    docids = set(x for x in index[i][term])
                    # if document we're looking at doesnt have term then break
                    if doc not in docids:
                        failed = True
                        break
                    # otherwise document has term so we can check the next one
                # whole sentence was present
                if not failed:
                    docs[i].add(doc)

        # now that we know which documents and titles contain the words of our phrase, we find which ones contain 
        # them in the right order
        for i in range(2):
            # check each document individually
            for doc in docs[i]:
                # whether we failed out of document because it was bad 
                failed = False
                # stores position lists for each term in sentence
                pos_list = {}
                # run through each word in sentence
                for term in sentence:
                    if doc in index[i][term]:
                        # stores positions of terms in documents, first element is current pointer second is position list
                        pos_list[term] = [0, index[i][term][str(doc)]]
                for pos in pos_list[sentence[0]][1]:
                    # work through each other term in sentence to see if it fits
                    for term_index, term in enumerate(sentence[1:]):
                        # check if position of term is 1 more than previous term
                        if pos_list[term][1][pos_list[term][0]] != pos_list[sentence[term_index]][1][pos_list[sentence[term_index]][0]] + 1:
                            failed = True
                            break 
                        pos_list[term][0] += 1 if len(pos_list[term][1]) == pos_list[term][0] else 0
                        failed = False

                if not failed:
                    if doc in posting_list:
                        # set sb to 1
                        posting_list[doc][i] = 1
                    else:
                        posting_list[doc] =  [i ^ 1, i]
        return posting_list
            
    elif node[0] == 'AND':
        l1 = evaluate_boolean_query(node[1])
        l2 = evaluate_boolean_query(node[2])
        return intersect(l1, l2)
    elif node[0] == 'OR':
        l1 = evaluate_boolean_query(node[1])
        l2 = evaluate_boolean_query(node[2])
        return union(l1, l2)
    else:
        raise Exception("*** UNRECOGNIZED QUERY NODE: " + str(node))

'''
Score(d,q) = (1-g) x sB(d,q) + g x sT(d,q)
This is the equation to find a documents zone score.
'''
def get_zone_score(posting_list, k, g = 0.7):
    score_list = []
    final = []
    for i in posting_list:
        score = ((1-g)*posting_list[i][0]) + (g * posting_list[i][1])
        score = round(score, 3)
        score_list.append((i, score))
    
    score_list = sorted(score_list, key = lambda x: x[1], reverse = True)

    for index in range(min(k, len(score_list))):
        final.append(score_list[index])

    return final

if __name__ == "__main__":
    INDEX_FILENAME = "zone_index.json"

    if len(argv) < 5:
        raise SyntaxError("Expected usage ./boolean_query.py [index dir] [k] [g] [query]")

    directory, k, g, query = argv[1:]

    try:
        index_file = open(directory + "/" + INDEX_FILENAME, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")
    
    index = json.loads([w for w in index_file][0])

    result = get_zone_score(evaluate_boolean_query(query_tree(query)), int(k), float(g));
    
    for doc in result:
        print(doc[0], doc[1])

#---------------UNIT TESTS-----------------

def test_query_tree():
    text = 'a AND b'
    query = query_tree(text)
    assert(query == ['AND', ('KEYWORD', 'a'), ('KEYWORD', 'b')])

    text = '(a AND b) OR c'
    query = query_tree(text)
    assert(query == ['OR', ['AND', ('KEYWORD', 'a'), ('KEYWORD', 'b')], ('KEYWORD', 'c')])

    text = '((a AND b) OR (c AND (d OR e)))'
    query = query_tree(text)
    assert(query == ['OR', ['AND', ('KEYWORD', 'a'), ('KEYWORD', 'b')], ['AND', ('KEYWORD', 'c'), ['OR', ('KEYWORD', 'd'), ('KEYWORD', 'e')]]])

def test_intersect():
	p1 = [1,2,3,6,13]
	p2 = [1,4,5,7,11,13,15]
	answer = intersect(p1,p2)
	assert(answer == (1,13))

	p1 = [1,2,4,5,6]
	p2 = [7,8,9,10]
	answer = intersect(p1,p2)
	assert(answer == tuple())

def test_union():
	p1 = [1,2,3,6,13]
	p2 = [1,4,5,7,11,13,15]
	answer = union(p1,p2)
	assert(answer == (1,2,3,4,5,6,7,11,13,15))

	p1 = [1,2,4,5,6]
	p2 = [7,8,9,10]
	answer = union(p1,p2)
	assert(answer == (1,2,4,5,6,7,8,9,10))

	p1 = [1,2,3,4]
	p2 = []
	answer = union(p1,p2)
	assert(answer == tuple(p1))


def test_zone_scoring():
    test_list = {1: [1, 1], 2: [1, 0], 8: [0, 1], 15: [0, 0]}

    assert(get_zone_score(test_list, 4, 0.65) == [(1,1.0), (8, 0.65), (2, 0.35), (15, 0.0)])
