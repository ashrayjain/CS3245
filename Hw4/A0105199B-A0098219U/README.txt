This is the README file for A0105199B-A0098219U-A0103516U-A0131729E's submission

Email: a0105199@u.nus.edu, a0098219@u.nus.edu, a0103516@u.nus.edu and a0131729@u.nus.edu


== General Notes about this assignment ==

Approaches for System Design:

--------------------------------------------------------------------
                           Approach 1:
--------------------------------------------------------------------

We create a vector space model (from HW3) for the words found in title and abstract fields found in the patsnap corpus. We now convert the query to a vector and rank the documents.

Performance: Below Baseline with average F2 = 0.287971786885619

Comments: A simple model to implement with a small set of documents to search. The low accuracy of this model is perhaps due to insufficient information available in the patent documents.    

--------------------------------------------------------------------
                           Approach 2:
--------------------------------------------------------------------

STEP 1: Use WIPO (World Intellectual Property Organization) IPC reports to map a word to the IPC codes that contain the word. For example, the IPC report for code B01D0001060000 contains the words "Evaporators with vertical tubes". Our approach creates a reverse index that maps a word to the IPC code.

STEP 2: Using the patsnap corpus provided, we create a trie that maps an IPC code to the patent number.

STEP 3: For every word in the query, we retrieve all the IPC codes in our reverse index from STEP 1. Then for all the IPC codes obtained from the index, we retrieve all the patent numbers from our trie in STEP 2. We the return this set of patent numbers.

Performance: Just below Baseline with average F2 = 0.339180935538332

Comments: A simple model that just retrieves all relevant patent numbers. However, as we do not consider other parameters such as document and term frequency, this design performs poorly as the patent numbers are unordered.

--------------------------------------------------------------------
                           Approach 3:
--------------------------------------------------------------------

Combined approach 1 and 2. We search for the query words in both the IPC reports from WIPO and the patsnap corpus (only title and abstract fields). This results in more documents returned as more patent numbers are matched.

Performance: Just above Baseline with average F2 = 0.362546790828216

--------------------------------------------------------------------
                           Approach 4:
--------------------------------------------------------------------

STEP 1: We use WIPO's suggested IPC categories tool (https://www3.wipo.int/ipccat) to retrieve the top 5 IPC categories for a given query.
STEP 2: For each of the 5 categories, we retrieve all the documents from the patsnap corpus that reference the category. We thus return all the documents that reference any of the 5 categories.

Performance: Above Baseline with average F2 = 0.421452312860265

Comments: Not only does this approach return fewer but more relevant patent numbers, it also has some degree of document ranking. This is because documents referencing the top IPC category from WIPO's tool are returned before documents that reference the bottom IPC category. However, the results suffer for query 3 and query 4 because the provided corpus doesn't contain (enough) patents for the categories that these queries map to.



== Files included with this submission ==

- index.py - wrapper script that does the command line i/o and passes the args to build_index.py
- build_index.py - main script that does the indexing
- dictionary.py - contains the implementation of a dictionary object
- postings.py - contains the implementation of a postings file object
- postings_list.py - contains the implementation of a postings list object. A postings file contains
                     a list of postings lists.
- argparse.py - argparse library for running on Sunfire
- search.py - does the command line i/o and passes each query to search_engine.py for evaluation.
              Also writes the results to output file.
- search_engine.py - runs the search engine algorithms on the input query and returns results
- scrape_wipo.py - runs on external server to scrape WIPO.

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0105199B-A0098219U-A0103516U-A0131729E, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0105199B-A0098219U-A0103516U-A0131729E, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

None
