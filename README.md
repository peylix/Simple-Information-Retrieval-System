# Simple-Information-Retrieval-System

Programming assignment for COMP3009J Information Retrieval.

A basic information retrieval system that is capable of performing preprocessing, indexing, retrieval (using BM25) and evaluation.

## How to run this project?

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