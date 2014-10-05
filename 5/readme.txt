CS662 - AI Programming
-----------------
Homework 5
Wei Fang
-----------------

Here is the structure of my folder.
weifang_5
©¦  20category
©¦  DFandD
©¦  weifang_5.py
©¦  tester.py
©¦  hCluster.py
©¸©¤readme.txt

20category is the dictionary pickled by the Function pickle_dict of Class corpus in weifang_5.py.
	20category = { category1: dict_TFIDF of category1, category2: dict_TFIDF of category2 ... category20: dict_TFIDF of category20}

DFandD is the list to store the corpus.DocumentFrequency and corpus.D.
	DFandD = [corpus.DocumentFrequency, corpus.D]

weifang_5.py is the program to load all files in the given directory and pickle 20category and DFandD. 
Please change the line 157 "   directory = "D:/usf/20_newsgroups"   " to your directory of 20_newsgroups.
It takes about 3 minutes to run this program.
	How to run: python weifang_5.py

tester.py is the program to test the classify function. 
It takes one command-line argument, which is the number of articles to try to classify. 
It loads two pickles "dict_TFIDF" and "DFandD".
And alse please change the line 7 "   directory = "D:/usf/20_newsgroups"   " to your directory of 20_newsgroups. 
The accuracy of classification fluctuates from 79% to 88% according to my test.
	How to run: python tester.py 100

hCluster.py is the program to perform hierarchical clustering.
It loads two pickles "dict_TFIDF" and "DFandD".
	How to run: python hCluster.py



