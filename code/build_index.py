'''

Reads all documents in the collection file into memory and writes
an inverted index to the processed folder.

The program will be run from the root of the repository.

'''

import sys
import json
from os.path import exists
from preprocessing import tokenize
from preprocessing import normalize


def read_documents(collection):
    '''
    Reads the documents in the collection (inside the 'collections' folder).
    '''

    assert type(collection) == str
    corpus_file = './collections/' + collection + '.ALL'

    # checks if it is a valid file.
    if not exists(corpus_file):
        print("- Error: File Doesn't Exist. -")
        sys.exit(1)
    
    documents = {}

    # opening the file.
    file = open(corpus_file, 'r')
    lines = file.readlines()
    key = 0

    # for loop to retrieve all documents and docID's
    for index in range(len(lines)):

        # checking if it is index.
        if lines[index][0:2] == '.I':
            key = int(lines[index].split()[1])

            # checking if the key already exists within the documents dictionary.
            if key in documents.keys():
                print("- Error: Key Already In Documents -")
                sys.exit(1)

            # setting the documents key: value pair.
            documents[key] = ''

        # checking if it is text (abstract).
        if lines[index][0:2] == '.W':
            temp = index + 1

            # adding text to the string until we encounter one of the five possible states.
            while temp < len(lines) and lines[temp][0:2] not in ['.I', '.T', '.A', '.W', '.X']:
                documents[key] += lines[temp]
                temp += 1

    # checking for missing values.
    for key in documents.keys():
        if documents[key] == '':
            print("- Error: Value Doesn't Exist For ID = " + str(key) + " - ")
            sys.exit(1)

    # closing the file
    file.close()    

    print(f'{len(documents)} documents read in total')
    return documents

def build_index(documents, s):
    '''
    Builds inverted index.
    '''

    assert type(documents) == dict

    index = {} 
    tokenized = {}
    
    # normalizing each document's text in preprocessing using a stemmer, 
    # and storing the result in tokenized.
    if s == 'l':
        method = 'lemmatization'
    else:
        method = 'stemming'
    
    for docID in documents:
        original_text = documents[docID]
        tokenized[docID] = normalize(tokenize(original_text), method)

    # Building the inverted index, with the number of documents (raw DF) in
    # index 0, and in index 1, we store the docID, the number of times it 
    # appears in the document, and the positions in the documents.
        
    for docID in documents:
        for temp in range(len(tokenized[docID])):

            # adding word as a key to the index, if not already in the index.
            if str(tokenized[docID][temp]) not in index:
                index[str(tokenized[docID][temp])] = [0, []]
                index[str(tokenized[docID][temp])][1].append([docID, 1, [temp + 1]])

            # otherwise, it's not our first encounter with the word, so we 
            # update the postings accordingly.
                
            else:
                # getting all the docID's referenced by the word.
                docIDs = [item[0] for item in index[str(tokenized[docID][temp])][1]]

                # if we already have the document listed, we update the counter (df) and
                # add the new position of the word.

                if docID in docIDs:
                    for item in index[str(tokenized[docID][temp])][1]:
                        if item[0] == docID:
                            item[1] += 1
                            item[2].append(temp + 1)
                
                # if the docID doesn't exist, we add a new set of attributes to 
                # the term.
                else:
                    index[str(tokenized[docID][temp])][1].append([docID, 1, [temp + 1]])

    # updating the raw DF in index 0 of the term.
    for term in index:
        index[term][0] = len(index[term][1])
    
    # sorting the index based on the terms and returning it.
    index = dict(sorted(index.items()))
    return index

def write_index(collection, index, method):
    '''
    Writes the data structure to the processed folder
    '''

    assert type(index) == dict
    extension = ".json" 
    index_file = './processed/' + collection + '_' + method + extension

    # checks if it is a valid file.
    if exists(index_file):
        print("- Error: Processed File Already Exists. -")
        sys.exit(1)

    # loading our dictionary into the json file appropriately,
    # so that it is readable and can be reloaded if required.
        
    file = open(index_file, 'w')
    file.write('{\n')
    count = 0

    for temp in index:
        count += 1
        file.write('\t')
        json.dump(temp, file)
        file.write(' : ')
        json.dump(index[temp], file)
        if count <= (len(index) - 1):
            file.write(',\n')
    
    file.write('\n}')
    file.close()

if __name__ == "__main__":
    '''
    main() function
    sys.argv[1] -> collection name
    '''

    # read the collection name from command line
    n = len(sys.argv)

    # Checking if correct number of command line arguements are provided
    if n != 2:
        print("- Error: Incorrect Number of Arguments -")
        sys.exit(1)
    
    # reading all documents, creating the index and writing it into a json file.
    documents = read_documents(sys.argv[1])
    method = 'l'
    index = build_index(documents, method)
    write_index(sys.argv[1], index, method)
    method = 's'
    index = build_index(documents, method)
    write_index(sys.argv[1], index, method)
    
    # prints success if everything has been executed properly.
    print("SUCCESS")
    exit(0)