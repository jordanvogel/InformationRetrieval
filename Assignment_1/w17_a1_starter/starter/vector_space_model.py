#
# CMPUT397 started code for programming assignment 1
#
# this module provides starter code with stubs of the
# functions to score keyword queries
#


from load_inverted_index import *
import math 

''' 
Implements the algorithm in Fig 6.14 of the textbook

NOTES: 

1. the code below is hard-coded for the running example; you
   should take it as a starting point only

2. the way IDF is computed (Eq. 6.7 on pg 108) is not robust
   to terms that appear in the whole corpus. FIX THIS.

3. The algorithm on Fig 6.14 DOES NOT normalize the vector
   based on the query vector, for efficiency. Thus scores
   can be higher than 1.0 !!!
'''
def cosineScore(index, query):
	#
	# TODO: FIX ME, SO I WORK FOR MORE THAN THE EXAMPLE ONLY
	#
	CORPUS_SIZE = 4
	Length_Vector = get_document_length_vector() 
	#
	#
	#
	Scores = {}
	for term in query:
		w_t_q = math.log( CORPUS_SIZE / index[term]['df'])
		for doc in index[term]['postings']:
			if doc in Scores:
				Scores[doc] += index[term]['postings'][doc]['tf-idf'] * w_t_q
			else:
				Scores[doc] = index[term]['postings'][doc]['tf-idf'] * w_t_q
	answer = []
	for doc in Scores:
		answer.append((doc, Scores[doc] / Length_Vector[doc]))
	return answer


'''
returns a vector with the 'length' of the documents
as in the algorithm of Fig 6.14. This is now done
by traversing the inverted index. This is inefficient!

TODO: change this so that you compute the vector once and
store it for future calls.
'''
def get_document_length_vector():
	doc_word_map = {}
	idx = get_hard_coded_inverted_index()
	for term in idx:
		for doc in idx[term]['postings']:
			if doc not in doc_word_map:
				doc_word_map[doc] = {term : idx[term]['postings'][doc]['tf-idf'] * 1.0}
			else:
				doc_word_map[doc][term] = idx[term]['postings'][doc]['tf-idf'] * 1.0
	vector = {}

	for doc in doc_word_map:
		Sum = 1.0
		for term in doc_word_map[doc]:
			#
			# IMPORTANT: the way the idf is computed in Eq 6.7 (pg 108)
			# does not account for terms that appear in every document
			# and thus have idf 0. We must skip them here.
			#
			Sum += doc_word_map[doc][term]*doc_word_map[doc][term]
		vector[doc] = math.sqrt(Sum)

	return vector



''' 
WRITE YOUR UNIT TESTS HERE
'''
if __name__ == "__main__":
	index = get_hard_coded_inverted_index()
	
	# simple test queries
	queries = [tuple(["system","retrieval"]), tuple(["a", "the"]), tuple(["recall"])]

	for query in queries:
		print "query: %s"%str(query)
		scores = cosineScore(index, query)
		scores.sort(key=lambda x: x[1], reverse=True)
		print "answer: %s"%str(scores)[1:-1]
		print

