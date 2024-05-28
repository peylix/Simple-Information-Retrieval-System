#!/usr/bin/env python3

import os
import string
import sys
import ast
from collections import Counter
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
    if len(sys.argv) == 5 and sys.argv[3] == '-p':
        path = sys.argv[4]

        if os.path.exists(path):
            file_path = os.path.join(path, file_name)

            if ignore_existence:
                return file_path
            elif os.path.exists(file_path):
                return file_path
            else:
                print('Error: The file does not exist. The current recognized file path is ', file_path)
                sys.exit(1)
        else:
            print('Error: The path does not exist.')
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./query_small_corpus.py -m <mode> -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def get_mode() -> str:
    '''
    This function gets the mode from the command line arguments.
    If the mode is not in the mode list or the arguments are not in the correct format, 
    the program will exit with an error message.

    Returns:
    str: the current mode.
    '''
    mode_list = ['interactive', 'automatic']
    if len(sys.argv) == 5 and sys.argv[1] == '-m':
        mode = sys.argv[2]
        if mode in mode_list:
            return mode
        else:
            print('Error: Invalid mode.')
            print('The available modes are: ', ', '.join(mode_list))
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./query_small_corpus.py -m <mode> -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def process_query(stopwords:list, query: str) -> list:
    '''
    This function is for conducting several preprocessing steps on the query.
    The steps include removing punctuation, stopwords, and stemming.

    Args:
    query (str): the query.

    Returns:
    list: a list containing the query words.
    '''

    p = porter.PorterStemmer()
    result = []
    stopwords_set = set(stopwords)
    translation_table = str.maketrans('', '', string.punctuation)

    for word in query.split():
        # Remove punctuation using the translation table
        # And convert the word to its lowercase
        word = word.lower().translate(translation_table)
        
        # Remove stopwords and check if the word is not empty
        if word and word not in stopwords_set:
            # Stem the word
            stemmed_word = p.stem(word)
            # Add the stemmed word to the result
            result.append(stemmed_word)

    return result


def find_relevant_documents(documents: dict, processed_query: list) -> dict:
    '''
    This function is for finding the relevant documents according to the given query.
    Since the BM25 scores are already computed, we only need to find the documents that contain the query words 
    and do some simple processing.

    Args:
    documents (dict): a dictionary containing the terms with the document IDs and their BM25 scores regarding the term.
    processed_query (list): a list containing the processed query words.

    Returns:
    dict: a dictionary containing the relevant document IDs and their BM25 similarity scores.
    '''
    result = {}
    for query_word in processed_query:
        if query_word in documents:
            result[query_word] = documents[query_word]
    
    # Map the values in result to Counters
    counters = map(Counter, result.values())

    # Merge the Counters
    merged_counter = dict(sum(counters, Counter()))

    # Sort the merged Counter by the BM25 score
    merged_counter = dict(sorted(merged_counter.items(), key=lambda item: item[1], reverse=True))

    return merged_counter




if __name__ == '__main__':
    mode = get_mode()
    path = get_path_of('documents')

    # Load the stopwords
    with open(get_path_of('files/stopwords.txt'), 'r') as file:
        stopwords = [word.strip() for word in file.readlines()]

    print(process_query(stopwords, 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft'))

    # Load the documents
    with open(path, 'r') as file:
        documents = ast.literal_eval(file.read())