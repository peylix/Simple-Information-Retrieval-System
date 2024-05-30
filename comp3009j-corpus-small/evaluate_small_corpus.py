#!/usr/bin/env python3

import sys
import os


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
        print('You can use `./evaluate_small_corpus.py -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def precision(ret: list, rel: list) -> float:
    '''
    This function calculates the precision of the retrieved documents.
    It means the proportion of the retrieved documents that are relevant.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the precision.
    '''
    return len(set(ret) & set(rel)) / len(ret)


def recall(ret: list, rel: list) -> float:
    '''
    This function calculates the recall of the retrieved documents.
    It means the proportion of the relevant documents that are retrieved.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the recall.
    '''
    return len(set(ret) & set(rel)) / len(rel)


def r_precision(ret: list, rel: list) -> float:
    '''
    This function calculates the R-Precision of the retrieved documents.
    It means how many relevant documents among the top R documents, 
    where R is the number of relevant documents.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the R-Precision.
    '''
    return len(set(ret[:len(rel)]) & set(rel)) / len(rel)


def precision_at_15(ret: list, rel: list) -> float:
    '''
    This function calculates the precision at 15 of the retrieved documents.
    It means the proportion of the first 15 retrieved documents that are relevant.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the precision at 15.
    '''
    return len(set(ret[:15]) & set(rel)) / 15


def ndcg_at_15(ret: list, rel: list) -> float:
    '''
    This function calculates the Normalized Discounted Cumulative Gain (NDCG) at 15 of the retrieved documents.
    It means how well the retrieved documents are ranked based on the relevance.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the NDCG at 15.
    '''
    dcg = 0
    for i, doc in enumerate(ret[:15]):
        if doc in rel:
            dcg += 1 / (i + 1)
    idcg = sum([1 / (i + 1) for i in range(min(len(rel), 15))])
    return dcg / idcg


def mean_average_precision(ret: list, rel: list) -> float:
    '''
    This function calculates the Mean Average Precision (MAP) of the retrieved documents.
    It means the average of the precision at each relevant document.

    Args:
    ret (list): a list of retrieved documents.
    rel (list): a list of relevant documents.

    Returns:
    float: the MAP.
    '''
    precision_sum = 0
    relevant_count = 0
    for i, doc in enumerate(ret):
        if doc in rel:
            relevant_count += 1
            precision_sum += relevant_count / (i + 1)
    return precision_sum / len(rel)


if __name__ == '__main__':
    queries_result = {}
    with open(get_path_of('21207464-small.results', 'r')) as file:
        current_query_id = ''
        for line in file:
            query_id = line.split()[0]
            if query_id != current_query_id:
                queries_result[query_id] = {}
                queries_result[query_id][line.split()[1]] = line.split()[3]
            else:
                queries_result[current_query_id][line.split()[1]] = line.split()[3]
            current_query_id = query_id
    


