#### readme ####
python sentiment.py

My program will run each file twice.
At the first time run without negation operations.
At the second time run with negation operations.

If you need to test another file, just comment everything associated with text1 and text2.

text1 = 'IntegratedCons.txt'
text2 = 'IntegratedPros.txt'

readtext(text1, positivewords, negativewords)      #first time run without negation operations
readtext(text2, positivewords, negativewords)      #first time run without negation operations
readtext_negation(text1, positivewords, negativewords)         #second time run with negation operations
readtext_negation(text2, positivewords, negativewords)	    #second time run with negation operations


Then uncomment the lines as below:
test = 'filename'
readtext(test, positivewords, negativewords)
readtext_negation(test, positivewords, negativewords)