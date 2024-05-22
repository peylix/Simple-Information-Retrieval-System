#!/usr/bin/env python3

import os
import sys
import string
from files import porter

p = porter.PorterStemmer()

def get_path_of(file_name: str, ignore_existence: bool = False) -> str:
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
                print('Error: The file does not exist. The current recognized file path is ', file_path)
                sys.exit(1)
        else:
            print('Error: The path does not exist.')
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./index_small_corpus.py -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def process_docs(documents: dict, stopwords: list) -> dict:
    result = {}
    stopwords_set = set(stopwords) # Using set can make the process faster
    # A translation table containing the rules for removing punctuation and digits
    translation_table = str.maketrans('', '', string.punctuation + string.digits)

    for document_name, words in documents.items():
        processed_words = []
        for word in words:
            # Remove punctuation and digits using the translation table
            # And convert the word to its lowercase
            word = word.lower().translate(translation_table)
            
            # Remove stopwords and check if the word is not empty
            if word and word not in stopwords_set:
                stemmed_word = p.stem(word)
                processed_words.append(stemmed_word)
        
        result[document_name] = processed_words

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

    documents = {}

    for document in sorted(os.listdir(get_path_of('documents')), key=lambda x: int(x) if x.isdigit() else x):
        file_path = get_path_of(f'documents/{document}')
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                documents[document] = content.split()
    documents = process_docs(documents, stopwords)
    
    print(documents)

    # Write the documents to a file
    with open(get_path_of('output.txt', ignore_existence=True), 'w') as file:
        for document in documents:
            file.write(f'{document}: {documents[document]}\n')
