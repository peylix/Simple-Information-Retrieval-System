#!/usr/bin/env python3

import os
import sys
import string
import time
import math
import json

from files import porter


def get_path_of(file_name: str, ignore_existence: bool = False) -> str:
    '''
    This function is for acquiring the file path of the given file name.
    It will get the path from the command line arguments if the arguments follow the correct format.
    If the file does not exist or the arguments are not in the correct format, 
    the program will exit with an error message.

    Args:
    file_name (str): the name of the file (may also includes part of the path).
    ignore_existence (bool): a flag to ignore the existence of the file (default False), can be used for writing files.

    Returns:
    str: the file path.
    '''
    if len(sys.argv) == 3 and sys.argv[1] == '-p':
        path = sys.argv[2]
        # print('the path is ', path)
        if os.path.exists(path):
            file_path = os.path.join(path, file_name)

            if ignore_existence:
                return file_path
            elif os.path.exists(file_path):
                return file_path
            else:
                print('Error: The file does not exist.')
                print('The current recognized file path is ', file_path)
                sys.exit(1)
        else:
            print('Error: The path does not exist.')
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./index_small_corpus.py -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def process_docs(documents: dict, stopwords: list) -> dict:
    '''
    This function is for conducting several preprocessing steps on the documents.
    The steps include removing punctuation, digits, stopwords, and stemming.

    Args:
    documents (dict): a dictionary containing the document ID and the words in the document.
    stopwords (list): a list of stopwords.

    Returns:
    dict: a dictionary containing the document ID and the processed words in the document.
    '''
    p = porter.PorterStemmer()
    result = {}
    stemmed_words_cache = {}
    stopwords_set = set(stopwords) # Using set to make the process faster
    # A translation table containing the rules for removing punctuation and digits
    translation_table = str.maketrans('', '', string.punctuation)

    for document_name, words in documents.items():
        processed_words = []
        for word in words:
            # Remove punctuation and digits using the translation table
            # And convert the word to its lowercase
            word = word.lower().translate(translation_table)
            
            # Remove stopwords and check if the word is not empty
            if word and word not in stopwords_set:
                if word not in stemmed_words_cache:
                    stemmed_words_cache[word] = p.stem(word)
                stemmed_word = stemmed_words_cache[word]
                processed_words.append(stemmed_word)
        
        result[document_name] = processed_words

    return result


def build_inverted_document_index(processed_documents: dict, k: float = 1.0, b: float = 0.75) -> dict:
    '''
    This function is for building the inverted index of the documents.
    The inverted index will be stored in a dictionary where the key is the term 
    and the value is a dictionary containing the document ID and the BM25 term frequency.

    Args:
    processed_documents (dict): a dictionary containing the document ID and the words processed by process_docs in the document.
    k (float): a constant value for BM25 (default 1.0).

    Returns:
    dict: a dictionary containing the term and the document ID with the BM25 term frequency.
    '''
    inverted_index = {}
    avg_doclen = sum([len(terms) for terms in processed_documents.values()]) / len(processed_documents) # Compute the average document length
    
    for document_id, terms in processed_documents.items():
        term_freq = {}

        for term in terms:
            if term in term_freq:
                term_freq[term] += 1
            else:
                term_freq[term] = 1
                
        # Compute the BM25 score for each term
        bm25_scores = {term: ((freq * (k + 1)) / (freq + k * ((1 - b) + (b * len(processed_documents[document_id]) / avg_doclen))))
                       for term, freq in term_freq.items()}
        
        for term, bm25_freq in bm25_scores.items():
            if term in inverted_index:
                inverted_index[term][document_id] = bm25_freq
            else:
                inverted_index[term] = {document_id: bm25_freq}
    
    return inverted_index


# Compute the document frequency in BM25
def compute_idf(inverted_index: dict, total_docs: int) -> dict:
    '''
    This function computes the inverse document frequency (or IDF) of the terms in the given inverted index.
    The IDF value here is calculated in alignment with the BM25 formula.

    Args:
    inverted_index (dict): a dictionary containing the term and the document ID with the BM25 term frequency.
    total_docs (int): the total number of documents.

    Returns:
    dict: a dictionary containing the term and the corresponding IDF value.
    '''
    idf = {}
    
    for term in inverted_index:
        idf[term] = math.log(1 + (total_docs - len(inverted_index[term]) + 0.5) / (len(inverted_index[term]) + 0.5))
    
    return idf
    

def build_bm25_weight_index(idf: dict, inverted_index: dict) -> dict:
    '''
    This function is for building the BM25 weight index of the documents.
    The BM25 weight index will be stored in a dictionary where the key is the term 
    and the value is a dictionary containing the document ID and the BM25 weights.

    Args:
    idf (dict): a dictionary containing the term and the corresponding IDF value.
    inverted_index (dict): a dictionary containing the term and the document ID with the BM25 term frequency.

    Returns:
    dict: a dictionary containing the term and the document ID with the BM25 weights.
    '''
    weight_index = {}
    
    for term in idf:
        weight_index[term] = {}

        for doc in inverted_index[term]:
            weight_index[term][doc] = idf[term] * inverted_index[term][doc]
        
        # Sort the index by the BM25 weights
        weight_index[term] = dict(sorted(weight_index[term].items(), key=lambda x: x[1], reverse=True))


    return weight_index


if __name__ == '__main__':
    start_time = time.process_time()
    print("+----------Start indexing...----------+")

    # Load the stopwords
    with open(get_path_of('files/stopwords.txt'), 'r') as file:
        stopwords = [word.strip() for word in file.readlines()]

    # Load the documents
    documents = {}
    for document in sorted(os.listdir(get_path_of('documents')), key=lambda x: int(x) if x.isdigit() else x):
        file_path = get_path_of(f'documents/{document}')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                documents[document] = content.split()

    current_time = time.process_time()
    print(f'{len(documents)} documents are loaded in {current_time - start_time} seconds.')

    # Process the documents
    documents = process_docs(documents, stopwords)
    current_time = time.process_time()
    print(f'{len(documents)} documents are processed in {current_time - start_time} seconds.')

    # Build the inverted index
    inverted_indexes = build_inverted_document_index(documents)
    current_time = time.process_time()
    print(f'Inverted indexes are built in {current_time - start_time} seconds.')

    # Compute the IDF
    idf = compute_idf(inverted_indexes, len(documents));
    current_time = time.process_time()
    print(f'IDF is computed in {current_time - start_time} seconds.')

    # Merge the inverted indexes and the IDF
    merged = {}
    for term in idf:
        merged[term] = {'idf': idf[term], 'docs': inverted_indexes[term]}
    
    # Build the BM25 weights index
    weights_index = build_bm25_weight_index(idf, inverted_indexes)

    # Write the documents to a file
    with open(get_path_of('21207464-small.index', ignore_existence=True), 'w') as file:
        json.dump(weights_index, file, indent=4)
    
    end_time = time.process_time()
    print(f'Indexing completed in {end_time - start_time} seconds.')
    
    print("+----------Indexing completed.----------+")
