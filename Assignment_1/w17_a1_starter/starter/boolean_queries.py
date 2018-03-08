#
# CMPUT397 started code for programming assignment 1
#
# this module provides starter code with stubs of the
# functions to answer boolean queries
#

from load_inverted_index import *

'''
Evaluates a boolean query as discussed in Chapters 1 and 2

Assumes the query is already optimized.

INPUT: tuple representing tree node:
   ('KEYWORD', keyword)
   ('PHARSE', "keyword_1 ... keyword_n")
   ('AND'/'OR', operand_1, operand_2)

Goes through each node, starting the recursion on the
"leftmost" operand if applicable.
'''
def evaluate_boolean_query(node):
	if node[0] == 'KEYWORD':
		#
		# TODO: fix me
		#
		return tuple(['doc1'])
	elif node[0] == 'PHRASE':
		#
		# TODO: fix me
		#
		return tuple(['doc2'])
	elif node[0] == 'AND':
		l1 = evaluate_boolean_query(node[1])
		l2 = evaluate_boolean_query(node[2])
		#
		# TODO: fix me
		#
		return l1 + l2
	elif node[0] == 'OR':
		l1 = evaluate_boolean_query(node[1])
		l2 = evaluate_boolean_query(node[2])
		#
		# TODO: fix me
		#
		return l1 + l2
	else:
		raise Exception("*** UNRECOGNIZED QUERY NODE: " + str(node))


'''
Parses a boolean query and returns a query tree.

INPUT: expression of the form:

<QUERY> :== <EXPRESSION> |
	    (<QUERY>) |
	    <QUERY> AND <QUERY> |
            <QUERY> OR <QUERY>
<EXPRESSION> :== <KW_EXPRESSION> | <PHRS_EXPRESSION>
<PHRS_EXPRESSION> :== "<KW_EXPRESSION>+"
<KW_EXPRESSION> :== any keyword

The parser must also tokenize the query in the same
that was used for tokenizing the corpus.
'''
def parse(expression):
	#
	# TODO: fix me
	#
	query = ('AND', ('AND', ('KEYWORD','stemming') ,('KEYWORD','off')), ('KEYWORD','of'))
	return query


'''
Estimates the size of a node in a query.

INPUT: tuple representing tree node:
   ('KEYWORD', keyword)
   ('PHARSE', "keyword_1 ... keyword_n")
   ('AND'/'OR', operand_1, operand_2)
'''
def estimate_size(node):
	if node[0] == 'KEYWORD':
		term = node[1]
		return len(inverted_index[term]['postings'])
	elif node[0] == 'PHRASE':
		#
		# TODO: fix me
		#
		return 1
	elif node[0] == 'AND':
		l1 = estimate_size(node[1])
		l2 = estimate_size(node[2])
		#
		# ASSUMPTION: the recursive query processor
		# will evaluate the sub-query in node[1] first
		#
		return l1 if l1<l2 else l2
	elif node[0] == 'OR':
		l1 = estimate_size(node[1])
		l2 = estimate_size(node[2])
		return l1 + l2
	else:
		raise Exception("*** UNRECOGNIZED QUERY NODE: " + str(node))


'''
Goes through the query tree recursively, swapping
sublists inside AND nodes, primarily
'''
def optimize(node):
    if node[0] == 'KEYWORD' or node[0] == 'PHRASE':
        return node
    elif node[0] == 'AND':
		#
		# TODO: check this is what we really want!
		#
        l1 = estimate_size(node[1])
        l2 = estimate_size(node[2])
        return node if l1<l2 else ('AND',optimize(node[2]),optimize(node[1]))
    elif node[0] == 'OR':
		#
		# TODO: check this is what we really want!
		#
        return ('OR',optimize(node[1]),optimize(node[2]))
    else:
        raise Exception("*** UNRECOGNIZED QUERY NODE: " + str(node))

    return node


'''
WRITE YOUR UNIT TESTS HERE
'''
if __name__ == "__main__":
    inverted_index = get_hard_coded_inverted_index()
    #
    # calls the parser and the optimizer
    #

    #
    # TEST CASE 1: should parse the raw query into the tuple representation
    # TEST CASE 2: should swap the order of both 'AND' nodes
    #
    raw_query = "(stemming AND off) AND of"
    parsed = ('AND', ('AND', ('KEYWORD','stemming') ,('KEYWORD','off')), ('KEYWORD','of'))
    optimized = ('AND', ('KEYWORD', 'of'), ('AND', ('KEYWORD', 'off'), ('KEYWORD', 'stemming')))

    query = parse(raw_query)
    print "PASS test_case 1" if query == parsed else "FAIL test_case 1"

    optimized_query = optimize(query)
    print "PASS test_case 2" if optimized == optimized_query else "FAIL test_case 2"

	#
	# then "executes" the query
	#
    print evaluate_boolean_query(optimized_query)
