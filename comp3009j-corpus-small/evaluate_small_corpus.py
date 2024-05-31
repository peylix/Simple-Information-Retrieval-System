#!/usr/bin/env python3

import math
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


def precision(ret: dict, rel: dict) -> float:
    '''
    This function calculates the precision of the retrieved documents.
    It means the proportion of the retrieved documents that are relevant.

    Args:
    ret (dict): a dictionary of retrieved documents in the format of {query_id: {doc_id: score}}.
    rel (dict): a dictionary of relevant documents in the format of {query_id: {doc_id: relevance}}.

    Returns:
    float: the precision.
    '''
    total_precision = 0
    for query_id in ret.keys():
        rel_ret = 0
        for doc_id in ret[query_id]:
            if doc_id in rel[query_id]:
                rel_ret += 1
        total_precision += rel_ret / len(ret[query_id])
    return total_precision / len(ret)


def recall(ret: dict, rel: dict) -> float:
    '''
    This function calculates the recall of the retrieved documents.
    It means the proportion of the relevant documents that are retrieved.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the recall.
    '''
    total_recall = 0
    for query_id in ret.keys():
        rel_ret = 0
        for doc_id in ret[query_id]:
            if doc_id in rel[query_id]:
                rel_ret += 1
        total_recall += rel_ret / len(rel[query_id])
    return total_recall / len(ret)


if __name__ == '__main__':
    queries_result = {}
    with open(get_path_of('21207464-small.results', 'r')) as file:
        current_query_id = ''
        for line in file:
            query_id = int(line.split()[0])
            doc_id = int(line.split()[1])
            score = float(line.split()[3])
            if query_id != current_query_id:
                queries_result[query_id] = {}
            queries_result[query_id][doc_id] = score
            current_query_id = query_id
    # print(queries_result)
    
    # Load the relevance judgments
    relevance_judgments = {}
    with open(get_path_of('files/qrels.txt'), 'r') as file:
        current_query_id = ''
        for line in file:
            query_id = int(line.split()[0])
            doc_id = int(line.split()[2])
            relevance = float(line.split()[3])
            if query_id != current_query_id:
                relevance_judgments[query_id] = {}
            relevance_judgments[query_id][doc_id] = relevance
            current_query_id = query_id
    # print(relevance_judgments)
    
    # Calculate the evaluation metrics
    print('+----------Evaluation Metrics----------+')
    # for query_id in queries_result:
    #     retrieved = list(queries_result[query_id].keys())
    #     relevant = relevance_judgments[int(query_id)]
    #     print(f'Query {query_id}:')
    #     print(f'Precision: {precision(retrieved, relevant)}')
    #     print(f'Recall: {recall(retrieved, relevant)}')
    #     print(f'R-Precision: {r_precision(retrieved, relevant)}')
    #     print(f'Precision at 15: {precision_at_15(retrieved, relevant)}')
    #     print(f'NDCG at 15: {ndcg_at_15(retrieved, relevant)}')
    #     print(f'Mean Average Precision: {mean_average_precision(retrieved, relevant)}')
    #     print()
    print('Precision:', precision(queries_result, relevance_judgments))
    print('Recall:', recall(queries_result, relevance_judgments))

    print('+--------------------------------------+')
