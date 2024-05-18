# COMP3009J Information Retrieval
## Small Document Corpus for Programming Assignment: Version 1.1
This file describes the contents of the corpus and associated files, along with their formats.

### Documents
The documents are contained in the [documents](documents) directory. Each file in this directory contains one document. The document ID is the filename. All files are plain text.

### Standard Queries
The file ``[queries.txt](files/queries.txt)'' contains the standard queries for evaluation.

Each query is on a new line, with the query ID before the query keywords. In total there are 225 queries.

### Relevance Judgments
The file ``[qrels.txt](files/qrels.txt)'' contains the relevance judgments. These are in the [format used by the TREC conference](https://trec.nist.gov/data/qrels_eng/).

Each line has 4 fields, separated by whitespace. The fields are as follows:

1.	The Query ID.
2.	(this field is always 0 and can be ignored)
3.	The Document ID.
4.	The relevance judgment. For judged relevant documents, a higher score means a higher level of relevance. Any document that does not appear in this file has been judged non-relevant.

In this corpus, there are no unjudged documents.

### Output Format
A sample output file (with randomly chosen documents) is shown in [sample_output.txt](files/sample_output.txt). This is the format your results should be in.

This file will have 4 fields on each line, which are:

1. The Query ID.
2. The Document ID.
3. The rank of the document in the results for this query (starting at 1).
4. The similarity score for the document and this query.

### Questions
If you have questions about this corpus, please post in the Brightspace discussion forum, or email me at [david.lillis@ucd.ie](mailto:david.lilli@ucd.ie).
