#!/usr/local/bin/python3
from shlex import split
from sys import argv
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import json
import itertools

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
    answer = []
    p1 = set(p1)
    p2 = set(p2)

    answer = p1.intersection(p2)

    return tuple(sorted(answer))

'''
Simple union operation for two posting lists
'''
def union(p1, p2):
    answer = []
    p1 = set(p1)
    p2 = set(p2)
    answer = p1.union(p2)

    return tuple(sorted(answer))

'''
Recursive query evaluation, taken from the sample starter code
'''
def evaluate_boolean_query(node):
    if node[0] == 'KEYWORD':
        posting_list = []
        if node[1] not in index[0]:
            return tuple()
        for item in index[0][node[1]]['postings']:
            posting_list.append(item[0])
        return tuple(posting_list)
    elif node[0] == 'PHRASE':
        posting_list = []
        for term in node[1].split():
            # if any word is not in the index, then the phrase is not
            if term not in index[0]:
                return tuple()
        sentence = node[1].split()
        for doc in index[0][sentence[0]]['postings']:
            indices = {}
            for term in sentence:
                docids = list(x[0] for x in index[0][term]['postings'])
                if doc[0] not in docids: 
                    break 
                else:
                    #indices[term] = (current index in position list, index of docid in posting list, value of position)
                    indices[term] = [0, docids.index(doc[0]), -1]
            if len(indices) != len(sentence):
                continue
            # loop through all pos in first term of sentence
            for pos in doc[1]['pos']:
                indices[sentence[0]][2] = pos

                # check against each other term
                for term_index, term in enumerate(sentence[1:]):
                    # position of term in doc
                    indices[term][2] = index[0][term]['postings'][indices[term][1]][1]['pos'][indices[term][0]]
                    # while the position of this term in doc is before the position of first term
                    while (indices[term][2] <= indices[sentence[term_index]][2]):
                        indices[term][0] += 1
                        if indices[term][0] >= len(index[0][term]['postings'][indices[term][1]][1]['pos']) - 1:
                            break
                        indices[term][2] = index[0][term]['postings'][indices[term][1]][1]['pos'][indices[term][0]]
                    # if this term is at the postition after first term
                    if indices[sentence[term_index]][2] + 1 == indices[term][2]:
                        if sentence[-1] == term:
                            posting_list.append(doc[0])
                        continue
                    else:
                        break
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

if __name__ == "__main__":
    INDEX_FILENAME = "index.json"

    if len(argv) < 3:
        raise SyntaxError("Expected usage ./boolean_query.py [index dir] [query]")

    directory = argv[1]
    query = argv[2]

    try:
        index_file = open(directory + "/" + INDEX_FILENAME, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No index file found in directory")
    
    index = json.loads([w for w in index_file][0])

    result = evaluate_boolean_query(query_tree(query))
    for doc in result:
        print(doc)


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
