'''

Runs query.py for a random set of queries (number given by user)
and ranks the retrieval based on the actual documents to be retrieved
(from .REL).

'''

import sys
import subprocess
import random

# finding the ranking of the first relevant document returned for query
def calculate_rank(relevant_docs, retrieved_docs):
    rank = 1                         # initializing a default value of rank 1 for the relevant doc for a query
    
    for doc_id in retrieved_docs:
        if doc_id in relevant_docs:
            return rank
        rank += 1
    
    return -1           # -1 if no relevant document found

def mrr(relevant, retrieved):
    total_reciprocal = 0
    # calculating rank for each query
    for query_id in relevant.keys():

        relevant_docs = relevant[query_id]
        retrieved_docs = retrieved[query_id]

        # ranking of the first relevant document returned for query
        rank = calculate_rank(relevant_docs, retrieved_docs)

        # calculating reciprocal for each query and adding it together for the sum of reciprocals
        if rank != -1:
            reciprocal = 1/rank
            total_reciprocal += reciprocal

    mrr_value = total_reciprocal/len(relevant)      # calculating the mrr value of all the queries

    return mrr_value

def compute_relevant_documents(relevant_docs, retrieved_docs):
    # initializing values
    summed_precision, number_of_relevant_documents, false_positive = 0, 0, 0
    
    # going through the retrieved documents' ID's
    for doc_id in retrieved_docs:

        # if it is a relevant document, we increment the number of relevant 
        # documents (true positive), find the precision (TP/ (TP+FP)), and
        # update summed_precision.
        if doc_id in relevant_docs:
            number_of_relevant_documents += 1
            temp = number_of_relevant_documents / (number_of_relevant_documents + false_positive)
            summed_precision += temp

        # otherwise, we increment false posiitve.
        else:
            false_positive += 1

    # to avoid 0 division.
    if number_of_relevant_documents != 0:
        # we return AveP = 
        # sum of precision of relevant and retrieved documents / number of relevant documents 
        return summed_precision / number_of_relevant_documents
    return 0
    
def map_k(relevant, retrieved, r):

    # initializing a MAP value to return.
    mean_average_precision = 0
    
    # going through each query in the relevant keys.
    for query_id in relevant.keys():
        relevant_docs = relevant[query_id]
        retrieved_docs = retrieved[query_id]

        # finding the average precision through compute_relevant_documents, which
        # finds the AveP (based on the formula in topic 5).
        average_precision = compute_relevant_documents(relevant_docs, retrieved_docs)
        
        # updating MAP accordingly.
        mean_average_precision += (average_precision / r)
    
    return mean_average_precision

def evaluation(program, collection, scheme, method, k, r, metric):

    file = open('./collections/' + collection + '.QRY', 'r')
    file1 = open('./collections/' + collection + '.REL', 'r')

    # initializing terms required for reading 10 queries from the CISI_simplified.QRY
    qry, qry_count, current_query_id, current_query_text = {}, 0, None, ""

    # reading and storing queries in a dictionary
    for line in file.readlines():          
        line = line.strip()  
        
        # check if line starts with '.I' which indicates a new query ID
        if line.startswith('.I'):
            
            # if there was a previous query, add it to the dictionary, 
            # reset query_text and increment qry_count.

            if current_query_id is not None:
                qry[current_query_id] = current_query_text.strip()  
                current_query_text = "" 
                qry_count += 1  
            
            # extract the query ID
            current_query_id = line.split()[1]  

        # skip lines starting with '.W' which are not needed for queries
        elif line.startswith('.W'):
            continue
        
        # if the line is not empty and doesn't start with '.W', add it to current query text
        elif line != '':
            current_query_text += line + ' '
    
    # add the last query if it exists
    if current_query_id is not None and current_query_text != "":
        qry[current_query_id] = current_query_text.strip()

    # picking r queries at random from the collection
    random_queries = random.choices(sorted(qry), k = r)

    # initialize a dictionary to store retrieved information
    retrieved = {}
    for i in random_queries: 
        answers = []
        # python3 ./code/query.py CISI_simplified ltn l 10 keyword
        output = subprocess.check_output(["python3", program, collection, scheme, method, str(k), qry[i]])
        output = output.decode('utf-8').strip()

        # appending all the docIDs returned by output into a list
        output_lines = output.split('\n')
        for line in output_lines:
            line = line.split()
            if line[0] not in answers:
                answers.append(int(line[0]))

        retrieved[i] = answers

    # initialize a dictionary to store relevance information
    relevant = {}
    for line in file1.readlines():
        line = line.split()  
        # initialize an empty list for the query ID if not present in the dictionary

        if line[0] not in retrieved.keys():
            continue

        if line[0] not in relevant.keys():
            relevant[line[0]] = [] 
        relevant[line[0]].append(int(line[1]))   # append the relevant document ID to the list corresponding to the query ID

    if metric == 'mrr':
        result = mrr(relevant, retrieved)
    else:
        result = map_k(relevant, retrieved, r)

    return result


if __name__ == "__main__":
    '''
    "main()" function goes here
    sys.argv[1] -> collection name
    sys.argv[2] -> 'ddd' scheme
    sys.argv[3] -> lemmatization (l) or stemming (s)
    sys.argv[4] -> number of documents wanted (k)
    sys.argv[5] -> number of random queries
    sys.argv[6] -> metric (MRR or MAP@k)
    eg. % python3 ./code/evaluation.py CISI_simplified ltn l 10 100 mrr
    '''
    # read the collection name from command line
    n = len(sys.argv)

    # Checking if correct number of command line arguements are provided
    if n != 7:
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

    # checking if the random number is a number and a positive number
    if sys.argv[5].isdigit() == False or int(sys.argv[5]) <= 0:
        print("- Error: Invalid Number of Random Queries. - ")

    if sys.argv[6] not in ['mrr','map']:
        print("- Error: Invalid Metric Input. - ")

    program = "./code/query.py"
    result = evaluation(program,sys.argv[1],sys.argv[2],sys.argv[3],k,int(sys.argv[5]),sys.argv[6])
    print('Program : ',sys.argv[0], ', Collection : ', sys.argv[1], ', Scheme : ', sys.argv[2], ', Method : ', sys.argv[3], ', K : ', sys.argv[4], ', Random : ', sys.argv[5], ', Metric : ', sys.argv[6], ' = ', str(result))

    exit(0)