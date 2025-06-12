'''

Reads in a collection name, a scoring scheme, k, and a keyword query 
and prints to STDOUT the IDs of the k documents in the collection 
with highest score, sorted by decreasing score

The program will be run from the root of the repository.

'''

import sys
import json
from os.path import exists
from preprocessing import tokenize
from preprocessing import normalize
import utils

def read_index(collection, method):
    '''
    Reads an inverted index (inside the 'processed' folder).
    '''
    extension = '.json'
    queries_file = './processed/' + collection + '_' + method + extension

    # checks if it is a valid file.
    if not exists(queries_file):
        print("- Error: File Doesn't Exist. -")
        sys.exit(1)
    
    # opening the file, loading the json data into index and
    # returning the index.

    file = open(queries_file)
    index = json.load(file)
    file.close()

    return index

def build_query_vector(keyword_query, method):
    '''
    Takes a query, tokenizes and normalizes it, builds a query vector
    using the 'nnn' weighting scheme.
    '''

    # taking the query terms and passing it through the same
    # stemmer used for the documents, to build the index if method is 's' otherwise lemmatization used for 'l'.

    terms = normalize(tokenize(keyword_query), method)
    query_vector = {}

    # building query vector, with the key as the term and 
    # value as the tf-idf score. Since we're using the 'nnn'
    # weighting scheme, we have tf = frequency of term, 
    # idf = 1 and normalization = 1.

    for term in terms:
        if term not in query_vector:
            query_vector[term] = 0
        query_vector[term] += 1
    
    query_vector = dict(sorted(query_vector.items()))
    return query_vector


def tokenize_and_answer(keyword_query, tf_scheme, df_scheme, normalization, k, s):
    '''
    Takes a query, tokenizes and normalizes it, builds a query vector, 
    and scores the documents using the dot product algorithm discussed in class,
    returns the k highest ranked documents in order.
    '''
    assert type(keyword_query) == str

    # setting up our query_vector for the method specified.
    if s == 'l':
        method = 'lemmatization'
    else:
        method = 'stemming'

    query_vector = build_query_vector(keyword_query, method)

    # valid_documents is a dictionary where we set the visited 
    # documents as the ID, and the value as the document_vector to
    # be normalized later, so Di = [wi1, wi2, .., win.]
    valid_documents = {}

    # temp is our indexing to make sure query_vector and each
    # document_vector stay consistent. In order to not get confused
    # with the inverted index, it will be referred to as temp.
    temp = 0 

    # computes the total number of documents in the index (utils.py).
    total_size = utils.number_of_documents(index)

    for token in query_vector:

        # handling OOV terms, by ignoring them and incrementing temp.
        if token not in index:
            temp += 1
            continue
        
        # otherwise, we take the DF from our index and all the details 
        # in the other element.
        raw_freq = index[token][0]

        for doc_details in index[token][1]:
            docID = doc_details[0]

            # if docID is not in valid_documents, we initialize it.
            if docID not in valid_documents:
                valid_documents[docID] = [0] * len(query_vector) 
            
            # computing the weight using the product of tf_compute
            # and df_compute (utils.py), and setting the document_vector
            # to the weight.
            weight = utils.tf_compute(tf_scheme, doc_details[1]) * utils.df_compute(df_scheme, total_size, raw_freq)
            valid_documents[docID][temp] = weight
        
        temp += 1

    # after weighting all the documents to the scheme, we compute query_values
    # which is the values in a list, and mod_query if normalization is cosine.
    query_values = list(query_vector.values())
    if normalization == 'c':
        mod_query = utils.mod_compute(query_values)

    # scoring all the documents
    for docID in valid_documents:

        # initialize the score to 0, and compute the dot product of query_values 
        # and valid_documents.
        score = 0
        for temp_index in range(len(valid_documents[docID])):
            score += (query_values[temp_index] * valid_documents[docID][temp_index])

        # for cosine normalization, we compute mod_documents, and decrease the score
        # by product of mod_documents and mod_query.
        if normalization == 'c':
            mod_documents = utils.mod_compute(valid_documents[docID])
            score = score / (mod_query * mod_documents)

        # setting valid_documents[docID] to score, replacing the weights.
        valid_documents[docID] = score
    
    # sorting our valid_documents using the docID as key.
    valid_documents = dict(sorted(valid_documents.items()))

    # building a min_heap (utils.py), where the heap is a list of 
    # tuples, where each tuple is (score, docID).
    min_heap = utils.heap(valid_documents)

    # finding the answer (utils.py), where the heap is a list of 
    # k tuples, where each tuple is (score, docID).
    answer = utils.largest(min_heap, k)

    return answer


index = {}

if __name__ == "__main__":
    '''
    "main()" function goes here
    sys.argv[1] -> collection name
    sys.argv[2] -> 'ddd' scheme
    sys.argv[3] -> lemmatization (l) or stemming (s)
    sys.argv[4] -> number of documents wanted (k)
    sys.argv[5] -> query
    eg. python3 ./code/query.py CISI_simplified ltn l 10 keyword
    '''
    # read the collection name from command line
    n = len(sys.argv)

    # Checking if correct number of command line arguements are provided
    if n != 6:
        print("- Error: Incorrect Number of Arguments -")
        sys.exit(1)

    # check if our 'ddd' scheme has correct length.
    if len(sys.argv[2]) != 3:
        print("- Error: Incorrect 'ddd' Scheme Input. -")
        sys.exit(1)

    # setting our scheme to all lowercase.
    sys.argv[2] = sys.argv[2].lower()

    # checking if tf scheme is one of ['l','n'].
    if sys.argv[2][0] not in ['l','n']:
        print("- Error: Incorrect 'tf' Input. -")
        sys.exit(1)

    # checking if idf scheme is one of ['t','n'].
    if sys.argv[2][1] not in ['t','n']:
        print("- Error: Incorrect 'idf' Input. -")
        sys.exit(1)

    # checking if normalization scheme is one of ['c','n'].
    if sys.argv[2][2] not in ['c','n']:
        print("- Error: Incorrect 'Normalization' Input. -")
        sys.exit(1)
    
    # checking if we can convert our string(k) into int(k).
    try:
        k = int(sys.argv[4])
    except ValueError:
        raise Exception("- Error: Incorrect Number of Documents Requested. - ")
    
    # checking if our k is lesser than or equal to 0.
    if k <= 0:
        print("- Error: Incorrect Number of Documents Requested. - ")
        sys.exit(1)
    
    # checking if lemmatization (l) or stemming (s) is mentioned
    if sys.argv[3] not in ['l','s']:
        print("- Error: Incorrect Specification for Lemmatization or Stemming. - ")

    # after these errors have been handled, we can read our index correctly.
    index = read_index(sys.argv[1], sys.argv[3])

    # once we've loaded our index correctly, we can find the documents relevant
    # to the query.
    answer = tokenize_and_answer(sys.argv[5], sys.argv[2][0], sys.argv[2][1], sys.argv[2][2], int(sys.argv[4]), sys.argv[3])

    # printing our answer in the given format.
    for score, docID in answer:
        print(docID, '\t', round(score, 3))
    
    exit(0)