#!/usr/bin/env python3

import os
import sys
from files import porter


def get_path_of(file_name: str) -> str:
    if len(sys.argv) != 3 or sys.argv[1] != '-p':
        print('Error: Invalid arguments.')
        print('You can use `./index_small_corpus.py -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)

    path = sys.argv[2]
    print('the path is ', path)
    if os.path.exists(path):
        file_path = os.path.join(path, file_name)

        if os.path.exists(file_path):
            return file_path
        else:
            print('Error: The file does not exist. The current recognized file path is ', file_path)
            sys.exit(1)

    else:
        print('Error: The path does not exist.')
        sys.exit(1)


def process_docs(documents: dict, stopwords: list) -> dict:
    result = {}
    for document in documents:
        for word in documents[document]:
            # Remove stopwords
            if word in stopwords:
                pass
            else:
                stemmed_word =  porter.stem(word.lower())
                # Create a list in the dictionary if the document is not in the dictionary
                if document not in result:
                    result[document] = []
                result[document].append(stemmed_word)
    return result


def get_all_terms(documents: dict) -> list:
    all_terms = []
    for document in documents:
        for word in documents[document]:
            if word not in all_terms:
                all_terms.append(word)
    return all_terms


def document_vector(documents: dict) -> dict:
    word_vectors = {}
    all_terms = get_all_terms(process_docs(documents))
    for document in documents:
        if document not in word_vectors:
            word_vectors[document] = [0] * len(all_terms)
        for word in documents[document]:
            if word in all_terms:
                word_vectors[document][all_terms.index(word)] = 1
    return word_vectors



if __name__ == '__main__':
    with open(get_path_of('files/stopwords.txt'), 'r') as file:
        stopwords = [word.strip() for word in file.readlines()] 

    print(stopwords)