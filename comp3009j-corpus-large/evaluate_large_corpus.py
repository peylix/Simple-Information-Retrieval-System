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
        print('You can use `./evaluate_large_corpus.py -p /path/to/comp3009j-corpus-large` to run the program.')
        sys.exit(1)


def precision(ret: dict, rel: dict) -> float:
    '''
    This function calculates the precision of the retrieved documents.
    It means the proportion of the retrieved documents that are relevant.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the precision.
    '''
    total_precision = 0
    for query_id in ret.keys():
        retrieved_docs = ret[query_id]
        relevant_docs = rel[query_id]
        # Count the number of relevant documents retrieved
        relevant_retrieved = sum(1 for doc in retrieved_docs if doc in relevant_docs and int(relevant_docs[doc]) > 0)

        precision = relevant_retrieved / len(retrieved_docs)

        total_precision += precision

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
        retrieved_docs = ret[query_id]
        relevant_docs = rel[query_id]
        # Count the number of relevant documents retrieved
        relevant_retrieved = sum(1 for doc in retrieved_docs if doc in relevant_docs and int(relevant_docs[doc]) > 0)
        # Total number of relevant documents
        total_relevant = sum(1 for doc in relevant_docs if int(relevant_docs[doc]) > 0)
        
        recall = relevant_retrieved / total_relevant
        
        total_recall += recall

    return total_recall / len(ret)


def r_precision(ret: dict, rel: dict) -> float:
    '''
    This function calculates the R-Precision of the retrieved documents.
    It means the precision of the top R documents, where R is the number of available relevant documents for the query.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the R-Precision.
    '''
    total_r_precision = 0

    for query_id in ret.keys():
        r = len(rel[query_id])
        relevant_in_top_r = 0

        for doc_id in list(ret[query_id].keys())[:r]:
            # check if the document is relevant and the relevance is greater than 0
            if doc_id in rel[query_id] and int(rel[query_id][doc_id]) > 0:
                relevant_in_top_r += 1

        total_r_precision += relevant_in_top_r / r

    return total_r_precision / len(ret)


def precision_at_k(ret: dict, rel: dict, k: int) -> float:
    '''
    This function calculates the precision at k of the retrieved documents.
    It means the proportion of the relevant documents in the top k retrieved documents.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the precision at k.
    '''
    total_precision_at_k = 0

    for query_id in ret.keys():
        relevant_in_top_k = 0

        for doc_id in list(ret[query_id].keys())[:k]:
            if doc_id in rel[query_id]:
                relevant_in_top_k += 1
                print('query id', query_id, 'doc id', doc_id, 'rel', relevant_in_top_k, 'k', k)
        precision_at_k = relevant_in_top_k / k

        total_precision_at_k += precision_at_k


    return total_precision_at_k / len(ret)


def mean_average_precision(ret: dict, rel: dict) -> float:
    '''
    This function calculates the mean average precision (MAP) of the retrieved documents.
    It means the average of the precision at each relevant document in the retrieved documents.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the mean average precision.
    '''
    total_map = 0

    for query_id in ret:
        map = 0
        relevant_documents_count = 0

        for i, doc_id in enumerate(ret[query_id], start=1):
            if doc_id in rel[query_id]:
                relevant_documents_count += 1
                map += relevant_documents_count / i
        total_map += map / len(rel[query_id])
        
    return total_map / len(ret)


def dcg_at_k(r: list, k: int) -> float:
    '''
    This function calculates the Discounted Cumulative Gain (DCG) at k of the retrieved documents.
    It means the sum of the relevance scores of the top k retrieved documents.

    Args:
    r (list): a list of relevance scores.
    k (int): the number of retrieved documents.
    
    Returns:
    float: the DCG at k.
    '''
    r = r[:k]
    if not r:
        return 0.0
    return r[0] + sum(relevance / math.log2(rank + 1) for rank, relevance in enumerate(r[1:], start=2))



def ndcg_at_k(ret: dict, rel: dict, k: int = 15) -> float:
    '''
    This function calculates the Normalized Discounted Cumulative Gain (NDCG) at k of the retrieved documents.
    It means the DCG at k divided by the Ideal DCG at k.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.
    k (int): the number of retrieved documents.
    '''
    ndcg_scores = {}
    for query_id, score_dict in ret.items():
        # Retrieve document scores and sort by descending score
        retrieved_docs = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
        retrieved_doc_ids = [doc_id for doc_id, _ in retrieved_docs]
        
        # Get relevance scores based on retrieved document ids
        actual_relevances = [rel.get(query_id, {}).get(doc_id, 0) for doc_id in retrieved_doc_ids]
        
        # Calculate DCG
        dcg = dcg_at_k(actual_relevances, k)
        
        # Sort documents by relevance to calculate IDCG
        ideal_relevances = sorted(rel.get(query_id, {}).values(), reverse=True)
        idcg = dcg_at_k(ideal_relevances, k)
        
        # if IDCG is zero, set NDCG to zero
        if idcg == 0:
            ndcg_scores[query_id] = 0.0
        else:
            ndcg_scores[query_id] = dcg / idcg
            
    return sum(ndcg_scores.values()) / len(ndcg_scores) if ndcg_scores else 0


def bpref(ret: dict, rel: dict) -> float:
    '''
    This function calculates the BPREF score of the retrieved documents.
    It means the proportion of non-relevant documents ranked lower than the relevant documents.

    Args:
    ret (dict): a dictionary of retrieved documents.
    rel (dict): a dictionary of relevant documents.

    Returns:
    float: the BPREF score.
    '''
    total_bpref_score = 0
    num_queries = 0

    # Iterate through each query
    for query_id in rel.keys():
        relevant_docs = {doc_id for doc_id, rel in rel[query_id].items() if rel > 0}
        non_relevant_docs = {doc_id for doc_id, rel in rel[query_id].items() if rel <= 0}

        if not relevant_docs:
            continue

        num_queries += 1
        
        R = len(relevant_docs)
        N = len(non_relevant_docs)
        score_sum = 0

        for r_doc in relevant_docs:
            # Count non-relevant docs ranked lower than the relevant doc r_doc
            count_B = sum(1 for n_doc in non_relevant_docs if ret[query_id].get(n_doc, 0) < ret[query_id].get(r_doc, 0))
            score_sum += count_B / N if N > 0 else 0

        # Calculate BPREF score for this query and add to total
        total_bpref_score += score_sum / R if R > 0 else 0

    # Calculate average BPREF score
    average_bpref = total_bpref_score / num_queries if num_queries > 0 else 0
    return average_bpref



if __name__ == '__main__':
    queries_result = {}
    with open(get_path_of('21207464-large.results', 'r')) as file:
        current_query_id = ''
        for line in file:
            query_id = int(line.split()[0])
            doc_id = line.split()[1]
            score = float(line.split()[3])
            if query_id != current_query_id:
                queries_result[query_id] = {}
            queries_result[query_id][doc_id] = score
            current_query_id = query_id

    
    # Load the relevance judgments
    relevance_judgments = {}
    with open(get_path_of('files/qrels.txt'), 'r') as file:
        current_query_id = ''
        for line in file:
            query_id = int(line.split()[0])
            doc_id = line.split()[2]
            relevance = float(line.split()[3])
            if query_id != current_query_id:
                relevance_judgments[query_id] = {}
            relevance_judgments[query_id][doc_id] = relevance
            # remove all the documents that are not relevant
            if relevance == 0:
                relevance_judgments[query_id].pop(doc_id)
            current_query_id = query_id


    
    # Calculate the evaluation metrics
    print('+----------Evaluation Metrics----------+')
    print(f'Precision: {precision(queries_result, relevance_judgments):.3f}')
    print(f'Recall: {recall(queries_result, relevance_judgments):.3f}')
    print(f'R-Precision: {r_precision(queries_result, relevance_judgments):.3f}')
    print(f'P@15: {precision_at_k(queries_result, relevance_judgments, 15):.3f}')
    print(f'MAP: {mean_average_precision(queries_result, relevance_judgments):.3f}')
    print(f'NDCG@15: {ndcg_at_k(queries_result, relevance_judgments):.3f}')
    print(f'bpref: {bpref(queries_result, relevance_judgments):.3f}')

    print('+--------------------------------------+')
