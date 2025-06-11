# Information Retrieval System

build_index.py: This system processes a collection of documents, queries, and relational documents to build an inverted index based on the provided method of normalization, which is done by stemming or lemmatization '''preprocessing.py'''.

query.py: This takes a query, normalizes and tokenizes the text into a query vector. Then, it finds the raw frequency produced by the inverted index, and ranks all documents for each token of the query by computing the dot product of the tf-idf weights, and the sppecified scoring scheme based on ltn.ltn. It allows for cosine normalization of these weights. After this is done for each query token, each document is scored (cosine normalization works here too), and using a heap, we find the k most relevant documents (k being specified by the user) for the query.

evaluation.py: 


