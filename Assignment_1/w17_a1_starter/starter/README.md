# a1_base_starter/README.md

This folder contains some starter code for boolean and ranked queries 
with the vector space model for the first programming assignment in
CMPUT397 W2017 term.

## Files Provided:

### boolean_queries.py

Has the (stub) code to parse queries from their textual expression
and code to execute such a query, recursively.

The main TODOS here are implementing the query processing algorithm
and then the parser (in this order).


### load_inverted_index.py

Has the code to load the inverted index from disk into a data structure
in memory. Note that the inverted index is needed everywhere, so you
should work out a way to load the index **once** and then 
**set all global variables** in all `module` files. 

Also has code to optimize a boolean query. Assuming the recursion is
done on the *left* subquery first, the optimization consists in 
checking the size of each operand in a query node with an `AND` operator
and swap them if needed.

The main TODOs here are fixing the code to estimate the size of a
query result.


One way to do so is to create constructor methods in all `module` files
and call them all once the data index is loaded.

### vector_space_model.py

Has the (stub) code to compute the Cosine Similarity as in Fig 6.14 of
the textbook. **READ THIS CAREFULLY** as there are many assumptions in 
the code and also in the algorithm in the textbook that are different
than what we have been talking in class.

The main TODO here is to make the code work with an inverted index
that you load from disk.

## Modules NOT included here

The main modules that you need to contribute yourself are:

1. creating an inverted index from a corpus
* dumping an inverted index to the screen


# WHAT ELSE?

You should **define** as many test cases as you can. Your evaluation will be
done based on test cases, besides readability of the code.

Make sure your code passess all test cases provided.

Ask for help **sooner** rather than later.

Finally, keep in mind that you don't need to reuse any of this code to do well
in the assignment. If you use this code, however, follow the UofA code of 
Student Conduct.
