# Simple Information Retrieval System

Programming assignment for COMP3009J Information Retrieval.

A basic information retrieval system that is capable of performing preprocessing, indexing, retrieval (using BM25) and evaluation.

The project can be divided into three modules: **Indexing**, **Querying** and **Evaluating**.

## How to run this project?

+ First change the permission of the file.

+ For running indexing programs (like `index_small_corpus.py` and `index_large_corpus.py`)

    ```shell
    ./index_small_corpus.py -p /path/to/comp3009j-corpus-small
    # or
    ./index_large_corpus.py -p /path/to/comp3009j-corpus-large
    ```

+ For running querying programs (like `query_small_corpus.py` and `query_large_corpus.py`)
  + In interactive mode

    ```shell
    ./query_small_corpus.py -m interactive -p /path/to/comp3009j-corpus-small
    # or
    ./query_large_corpus.py -m interactive -p /path/to/comp3009j-corpus-large
    ```

  + In automatic mode

    ```shell
    ./query_small_corpus.py -m automatic -p /path/to/comp3009j-corpus-small
    # or
    ./query_large_corpus.py -m automatic -p /path/to/comp3009j-corpus-large
    ```

+ For running the evaluation programs (like `evaluate_small_corpus.py` and `evaluate_large_corpus.py`)

    ```shell
    ./evaluate_small_corpus.py -p /path/to/comp3009j-corpus-small
    # or
    ./evaluate_large_corpus.py -p /path/to/comp3009j-corpus-large
    ```

## Explanation

### Indexing

This module will produce a file named `<ucd_id>-small.index` or `<ucd_id>-large.index` where all the indexes are organized in a JSON format such as:

```JSON
{
  "term": {
    "file-id": "BM25 weight",
    ...
  },
  ...
}
```

### Querying

This module search through the files under the directory `../documents/`. It hehaves slightly differently in different modes.

In the *interactive mode*, the program will take your query and print out the results immediately. The format of the result is as follow:

| Query ID | <always 0 in the *interactive mode*> | Document ID | Relevance Judgment |

In the *automatic mode*, the program will automatically search through the documents based on the queries in `../queries.txt` and save the results in a file named `<ucd_id>-small.results` or `<ucd_id>-large.results`. The results will be in a format similar to those in the *interactive mode*.

| Query ID | Document ID | Rank of the Document | Similarity Score |

### Evaluating

This module is aimed to evaluate the results of the querying module. It uses the following evaluation metrics:

+ Precision
+ Recall
+ R-Precision
+ Precision at K
+ Mean Average Precision (MAP)
+ Normalized Discounted Cumulative Gain (NDCG)
+ Binary Preference (for large corpus only)
