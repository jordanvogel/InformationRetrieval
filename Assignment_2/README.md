# CMPUT397A1

Program Usage.
    Part 1
        ./create_zone_index.py [document dir] [index dir]
        ./zone_scorer.py [index dir] [k] [g] [q]

    Part 2
       ./create_labeled_index.py [document dir] [index dir]
       ./knn_classifier.py [index dir] [k] [q] 

    Part 3
        ./create_index.py [document dir] [index dir]
        ./k_means_clusterer.py [index dir] [k] [optional id_1 id_2 ... id_k]
            The assumption we make is that for the optional ids, either k or 0 ids will be provided

        Even though it looks like it only ever does 1 reassignment, we tested the clustering on the 2k docs from assignment1, and it did 13 reassignments and took 2100s (pretty much forever) but worked. We believe it only does 1 reassignment since the documents are so similar in the test data we are given.


How to run unit tests for each file
        -zone_scorer.py: Test names are 'test_query_tree()', 'test_intersect()', 'test_union()', 'test_zone_scoring()'

        -create_labeled_index.py: Test names are 'test_bin_search()', 'test_lambda_sort()', 'test_punct_remove()' 
        -knn_classifier.py: Test names are 'test_punct_remove()', 'test_cosineScore()', 'test_rank_result()'

        -create_index.py: Test names are 'test_bin_search()', 'test_lambda_sort()', 'test_punct_remove()'
        -k_means_clusterer.py: Test names are 
