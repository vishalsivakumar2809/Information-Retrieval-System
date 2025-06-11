# Information Retrieval System

build_index.py: This system processes a collection of documents, queries, and relational documents to build an inverted index based on the provided method of normalization, which is done by stemming or lemmatization '''preprocessing.py'''.

query.py: This takes a query, normalizes and tokenizes the text into a query vector. Then, it finds the raw frequency produced by the inverted index, and ranks all documents for each token of the query by computing the dot product of the tf-idf weights, and the sppecified scoring scheme based on ltn.ltn. It allows for cosine normalization of these weights. After this is done for each query token, each document is scored (cosine normalization works here too), and using a heap, we find the k highest scored documents (k being specified by the user) for the query.

evaluation.py: This uses '''query.py''' to find all the retrieved documents, and the actual relevant documents, and evaluates the schemes accordingly. It does so using MAP or MRR scoring, which is used to determine the correctness of the IR system.

testfile.py: Runs evaluation.py with different scoring schemes, evaluation metrics, normalization techniques, different final number of retrieved documents, randomly selecting a number of queries, to find the best techniques for the IR system. Do note that running it with the current metrics takes roughly 3-4 hours to run, and a few sample runs are provided in the samples directory.

