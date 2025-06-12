'''
Additional functions to assist in query.py.
'''
import math
import heapq

def number_of_documents(index):
    '''
    Computes the total number of documents in the index.
    '''
    count = 0
    encounterred_documents = {}

    # for loop to traverse through the index dictionary.
    for token in index:
        for doc_details in index[token][1]:
            
            # increments count only if the document hasn't been seen before.
            if doc_details[0] not in encounterred_documents:
                encounterred_documents[doc_details[0]] = 0
                count += 1

    return count

def tf_compute(tf_scheme, freq):
    '''
    Computes the tf score, given the scheme and frequency
    of terms within the document.
    '''
    # computes the logarithmic tf.
    if tf_scheme == 'l':
        return 1 + math.log(freq, 10) 
    
    # returns the natural tf.
    return freq
    
def df_compute(df_scheme, total_size, raw_freq):
    '''
    Computes the idf score, given the scheme, total number of
    documents and number of documents that the term is present.
    '''
    # computes the standard idf.
    if df_scheme == 't':
        return math.log(total_size/raw_freq, 10)
    
    # computes the natural idf.
    return 1

def mod_compute(values):
    '''
    Computes the modulus of a list of values.
    '''
    sum = 0
    for value in values:
        sum += value * value

    sum = math.sqrt(sum)
    return sum

def heap(valid_documents):
    '''
    Builds a min_heap using the heapq library.
    '''

    # List to hold items from dictionary,
    heap_list = []

    # we append into the list as a pair of score, docID.
    for key, value in valid_documents.items():
        heap_list.append((value, key))
    
    # heapify the items.
    heapq.heapify(heap_list)
    return heap_list

def largest(min_heap, n):
    '''
    Returns the k largest documents from a min_heap 
    using the heapq library.
    '''

    # this line computes all of the n largest scores within
    # the min_heap, but the ties are handled differently i.e.
    # the ties sort by decreasing docID if the scores are the 
    # same.
    min_heap = heapq.nlargest(n, min_heap)

    # we fix this by traversing through min_heap and resorting
    # the tie cases.
    encounterred_scores = []
    answer = []
    for i in range(len(min_heap)):
        k, v = min_heap[i][0], min_heap[i][1]

        # we've not encounttered the key yet, so we add to the
        # answer.
        if k not in encounterred_scores:
            encounterred_scores.append(k)
            answer.append((k, v))
        
        # we've encounttered the key, so we check how many spaces
        # back we need to go to add the new pair, as this'll be 
        # our lowest docID for the score.
        else:
            temp = i
            while answer[temp - 1][0] == k:
                temp -= 1
                if temp == -1:
                    break
            answer.insert(temp, (k, v))
            
    return answer
