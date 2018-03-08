# CMPUT397A1

Program Usage.
    -creating the index: ./create_index [dir]

    -printing the index: ./print_index [dir]

    -doing boolean queries: ./boolean_query [dir] [query]
        the query must be wrapped in single quotes, with phrases wrapped in double quotes
        I.E query = 'a AND (b OR c) AND "not even once"'

    -getting vector scores: ./vs_query [dir] [k(INT)] [scores(y/n)] [term_1] [term_2] ... [term_n]




How to run unit tests for each file.
	-create_index.py: The tests are 'test_bin_search()', 'test_lambda_sort()', 'test_punct_remove()'

        -boolean_query.py: Test names are 'test_query_tree()', 'test_intersect()', 'test_union()'

        -print_index.py: Test name is 'test_print_index()', ,there is only one test file as it covers all the functionality of the program

        -vs_query.py: Test names are: 'test_cosineScore()', 'test_rank_results()', there are only two functions here as our method of getting the tf-idf scoring is done during the creating of the index
