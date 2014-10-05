#####    readme    #####
#####    please use my readARFF.py   #####


1. change the dataset to the filename

line 392
    if __name__ == '__main__' :
    dataset = 'filename of the dataset'


    For example: 
        # dataset = 'tennis.arff'
        # dataset = 'restaurant.arff'
        # dataset = 'breast-cancer.arff'
        # dataset = 'nursery.arff'
        dataset = 'lymphography.arff'

2. execute the decisionTree.py
    python decisionTree.py

    Then I will print the precision, recall and accuracy of decision tree and zeroR algorithm in the format as below.

    #####   lymphography.arff dataset   #####
    #####   The performance of decision tree   #####
         test_precision:
           ['3:84.37%', '2:82.00%', '4:25.00%']
         test_recall:
           ['3:72.72%', '2:89.23%', '4:25.00%']
         test_accuracy: 80.000000%

         training_precision:
           ['1:100.00%', '3:100.00%', '2:100.00%', '4:100.00%']
         training_recall:
           ['1:100.00%', '3:100.00%', '2:100.00%', '4:100.00%']
         training_accuracy: 100.000000%
    #####   The performance of zeroR   #####
         test_precision:
           ['3:20.62%', '2:33.12%', '4:0.00%']
         test_recall:
           ['3:40.00%', '2:60.00%', '4:0.00%']
         test_accuracy: 53.750000%

         training_precision:
           ['1:0.00%', '3:0.00%', '2:55.34%', '4:0.00%']
         training_recall:
           ['1:0.00%', '3:0.00%', '2:100.00%', '4:0.00%']
         training_accuracy: 55.344828%


PS: The program can print the decision tree, if uncomment the line 315 and line 316.
