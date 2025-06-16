# Information Retrieval System

This project implements a modular Information Retrieval (IR) system for indexing, querying, scoring, and evaluating a collection of documents using tf-idf and standard IR metrics.

## ```build_index.py```
Builds an inverted index from raw documents and relevance data.

Supports normalization via stemming or lemmatization (```preprocessing.py```).

Outputs an index with term frequencies and document stats.

## ```query.py```
Processes and scores queries against the inverted index.

Normalizes and tokenizes queries into tf-idf vectors.

Supports scoring schemes (ex: ltn.ltn) and optional cosine normalization.

Returns top-k documents using a heap-based ranking.

## ```evaluation.py```
Evaluates retrieval performance.

Compares retrieved results with relevant documents.

Supports MAP and MRR as evaluation metrics.

## ```testfile.py```
Runs automated experiments across different configurations.

Tests scoring schemes, normalization methods, evaluation metrics, and k-values.

Randomly samples queries for benchmarking.

Full runs may take 3–4 hours; samples are in the ```samples/``` directory.

# Execute

```
Reading the .ALL collection:
1: python3 ./code/build_index.py CISI_simplified

Finding the top 10 relevant documents to a query [NOTE: collection, queries, scoring scheme, method, and number of retrieved documents can be altered]:
2. python3 ./code/query.py CISI_simplified ltn l 10 "What is information science?  Give definitions where possible."

Evaluating query.py through the various metrics [NOTE: scoring scheme, method, number of random queries, number of retrieved documents and metrics can be altered]:
3. python3 ./code/evaluation.py CISI_simplified ltn l 10 10 mrr

Testing all possible scoring schemes, methods, number of random queries [10, 80], number of retrieved documents [10, 860, 1710] and metrics, a number of times:
4. python3 ./code/testfile.py```


