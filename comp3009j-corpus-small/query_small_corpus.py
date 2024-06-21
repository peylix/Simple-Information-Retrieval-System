#!/usr/bin/env python3

import os
import string
import sys
import json
import time

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


def find_relevant_documents(index: dict, processed_query: list) -> dict:
    '''
    This function is for finding the relevant documents according to the given query.
    Since the BM25 scores are already computed, we only need to find the documents that contain the query words 
    and do some simple processing.
    I use Counter to store the BM25 scores to avoid duplicates and boost the performance as well as make the code neater.

    Args:
    documents (dict): a dictionary containing the terms with the document IDs and their BM25 scores regarding the term.
    processed_query (list): a list containing the processed query words.

    Returns:
    dict: a dictionary containing the relevant document IDs and their BM25 weights.
    '''
    result = Counter() # Using Counter to store the BM25 scores to avoid duplicates

    for query_word in processed_query:
        if query_word in index:
            result.update(index[query_word])
    
    # Sort the result by the BM25 score
    sorted_result = dict(result.most_common())

    return sorted_result


def format_output(current_query_number: int, relevant_documents: dict, mode: str) -> str:
    '''
    This function is for adjusting the relevant documents to make it align with the required format.

    Args:
    relevant_documents (dict): a dictionary containing the relevant document IDs and their BM25 weights.

    Returns:
    str: the formatted output.
    '''
    result = ''
    rank_count = 1
    if mode == 'automatic':
        for document_id, score in relevant_documents.items():
            result += f'{current_query_number} {document_id} {rank_count} {score}\n'
            rank_count += 1
            if rank_count > 15:
                break
    elif mode == 'interactive':
        for document_id, score in relevant_documents.items():
            result += f'{rank_count} {document_id} {score}\n'
            rank_count += 1
            if rank_count > 15:
                break
    return result
    


if __name__ == '__main__':
    start_time = time.process_time()
    print("+----------Start querying----------+")

    mode = get_mode()
    path = get_path_of('documents')

    # Load the stopwords
    with open(get_path_of('files/stopwords.txt'), 'r') as file:
        stopwords = [word.strip() for word in file.readlines()]

    # Load the documents
    with open(get_path_of('21207464-small.index'), 'r') as file:
        built_index = json.load(file)
    current_time = time.process_time()
    print(f'{len(built_index)} terms are loaded in {current_time - start_time} seconds.')

    if mode == 'automatic':
        print('**You are using the automatic mode. The queries will be carried out automatically.**')

        with open(get_path_of('files/queries.txt'), 'r') as file:
            lines = file.readlines()
            
        current_time = time.process_time()
        print(f'{len(lines)} queries are loaded in {current_time - start_time} seconds.')

        with open(get_path_of('21207464-small.results', ignore_existence=True), 'w') as file:
            for line in lines:
                # Split the line into two parts
                # The first part is the query ID and the second part is the query
                query_id, query = line.strip().split(maxsplit=1)
                processed_query = process_query(stopwords, query)
                relevant_documents = find_relevant_documents(built_index, processed_query)
                file.write(format_output(int(query_id), relevant_documents, mode='automatic'))

        end_time = time.process_time()
        print(f'The results are computed in {end_time - start_time} seconds.')
    elif mode == 'interactive':
        print('**You are using the interactive mode. Enter "QUIT" to exit.**')

        while True:
            query = input('> Please enter your query: ')
            if query == 'QUIT':
                break
            begin_query_time = time.process_time()
            processed_query = process_query(stopwords, query)
            relevant_documents = find_relevant_documents(built_index, processed_query)
            print(format_output(1, relevant_documents, mode='interactive'))

            end_query_time = time.process_time()
            print(f'This query is processed within {begin_query_time - end_query_time} seconds.')
    
    print("+----------Querying Ended----------+")
