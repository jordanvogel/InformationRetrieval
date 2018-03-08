#
# CMPUT397 started code for programming assignment 1
#
# this module provides functions to load the inverted index
# from a file/directory/sqlite database

import math

''' 
returns a hard-coded inverted index from the example 
''' 
def get_hard_coded_inverted_index():
	example_inverted_index = {
	'a' : {'df': 3, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.1249387366, 'pos' : tuple([1])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.1249387366, 'pos' : tuple([1])} ,
			'doc4' : {'tf' : 2, 'tf-idf' : 0.2498774732, 'pos' : (12,20)}
		}
	},
	'at' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([5])}
		}
	},
	'be' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([3])}
		}
	},
	'boolean' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([3])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([3])}
		}
	},
	'but' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([8])}
		}
	},
	'chops' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([15])}
		}
	},
	'ending' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([18])}
		}
	},
	'in' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([1])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([1])}
		}
	},
	'increases' : {'df': 1, 
		'postings' : {
			'doc3' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([2])}
		}
	},
	'indexing' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([6])}
		}
	},
	'invoked' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([4])}
		}
	},
	'lowers' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([8])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([8])}
		}
	},
	'never' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([7])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([7])}
		}
	},
	'not' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([9])}
		}
	},
	'of' : {'df': 1, 
		'postings' : {
			'doc3' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([5])}
		}
	},
	'off' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([16])}
		}
	},
	'precision' : {'df': 1, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([9])}
		}
	},
	'processing' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([11])}
		}
	},
	'query' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([13])}
		}
	},
	'recall' : {'df': 1, 
		'postings' : {
			'doc2' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([9])}
		}
	},
	'retrieval' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([4])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([4])}
		}
	},
	'should' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([2])}
		}
	},
	'size' : {'df': 1, 
		'postings' : {
			'doc3' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([4])}
		}
	},
	'stemming' : {'df': 4, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0, 'pos' : tuple([6])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0, 'pos' : tuple([6])} ,
			'doc3' : {'tf' : 1, 'tf-idf' : 0, 'pos' : tuple([1])} ,
			'doc4' : {'tf' : 2, 'tf-idf' : 0, 'pos' : (1,14)}
		}
	},
	'system' : {'df': 2, 
		'postings' : {
			'doc1' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([5])} ,
			'doc2' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([5])}
		}
	},
	'the' : {'df': 2, 
		'postings' : {
			'doc3' : {'tf' : 2, 'tf-idf' : 0.6020599913, 'pos' : (3,6)} ,
			'doc4' : {'tf' : 1, 'tf-idf' : 0.3010299957, 'pos' : tuple([17])}
		}
	},
	'time' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([7])}
		}
	},
	'vocabulary' : {'df': 1, 
		'postings' : {
			'doc3' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([7])}
		}
	},
	'while' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([10])}
		}
	},
	'word' : {'df': 1, 
		'postings' : {
			'doc4' : {'tf' : 1, 'tf-idf' : 0.6020599913, 'pos' : tuple([21])}
		}
	}
	}
	return example_inverted_index


'''
goes through an inverted index and checks that the
df and tf values agree with the posting lists. 
 '''	
def check_inverted_index(idx):
	for term in idx:
		documents = idx[term]['postings']
		if idx[term]['df'] != len(documents):
			print "*** ERROR *** 'df' for term <" + term + "> is wrong"
			print idx[term]
			return "FAIL"
		for doc in documents:
			if idx[term]['postings'][doc]['tf'] != len(idx[term]['postings'][doc]['pos']):
				print "*** ERROR *** 'tf' for term <" + term + "> is wrong"
				print idx[term]['postings'][doc]
				return "FAIL"
	return "PASS"

'''
Returns the inverted index

TODO: load the inverted index from disk 
	for now, returns a hard-coded one
'''
def get_inverted_index():
	index = get_hard_coded_inverted_index()
	if check_inverted_index(index) == "PASS":
		return index

''' 
WRITE YOUR UNIT TESTS HERE
'''
if __name__ == "__main__":
	print check_inverted_index(get_hard_coded_inverted_index())
