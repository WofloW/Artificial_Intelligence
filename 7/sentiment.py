import sys,re,string

negationwords = ["won't", "wouldn't", "shan't", "shouldn't", "can't", 'cannot', "couldn't", "mustn't", "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", "hadn't", "doesn't", "don't", "didn't", 'not', 'no', 'never']
negationdict = {}
for item in negationwords:
    negationdict[item] = None
delimiters =[',', '.', ';', '-']

def readsentiment(filename):
    filehandle = open(filename)
    dict1 = {}
    ### remove all commented and blank lines.
    text = [line.strip() for line in filehandle.readlines() if not line.startswith(';') and len(line) > 1]
    for item in text:
        dict1[item] = None
    return dict1
    
def readtext(filename, pos, neg) :
    filehandle = open(filename)
    ### remove all commented and blank lines.
    lines = [line.strip() for line in filehandle.readlines() if not line.startswith('%') and len(line) > 1]
    class_text = re.search('<(\w{4})>.*</\w{4}>',lines[0]).groups()[0]
    texts = [re.search('<\w{4}>(.*)</\w{4}>',line).groups() for line in lines if re.search('<\w{4}>(.*)</\w{4}>',line)]
    
    right = 0
    for text in texts:
        pro = 0
        con = 0
        judge = None
        for word in text[0].split():
            word = word.strip(string.punctuation)
            if word in pos:
                pro += 1
            elif word in neg:
                con += 1

        if pro > con:
            judge = 'Pros'
        else:
            judge = 'Cons'
        if judge == class_text:
            right += 1
    accuracy = float(right)/len(texts)
    print "##### %s #####" %filename
    print "accuracy = %.2f%%" %(accuracy*100) 



def readtext_negation(filename, pos, neg) :
    filehandle = open(filename)
    ### remove all commented and blank lines.
    lines = [line.strip() for line in filehandle.readlines() if not line.startswith('%') and len(line) > 1]
    class_text = re.search('<(\w{4})>.*</\w{4}>',lines[0]).groups()[0]
    texts = [re.search('<\w{4}>(.*)</\w{4}>',line).groups() for line in lines if re.search('<\w{4}>(.*)</\w{4}>',line)]
    
    
    right = 0
    for text in texts:
        pro = 0
        con = 0
        judge = None
        negationflag = False
        negationendflag = False
        for word in text[0].split():
            if negationflag:                #detect the end of flipping sentiment
                for item in delimiters:
                    if item in word:
                        negationendflag = True
                        break
            word = word.strip(string.punctuation)
            
            if word in pos:
                if negationflag == False:
                    pro += 1
                else:
                    con += 1
                    
            elif word in neg:
                if negationflag == False:
                    con += 1
                else:
                    pro += 1

            if word in negationdict:
                negationflag = True
            if negationendflag:         #end the flipping sentiment after operating the last word
                negationflag = False
                negationendflag = False

        if pro > con:
            judge = 'Pros'
        else:
            judge = 'Cons'
        if judge == class_text:
            right += 1
    accuracy = float(right)/len(texts)
    print "##### %s with negation #####" %filename
    print "accuracy = %.2f%%" %(accuracy*100) 


if __name__ == '__main__' :
    text1 = 'IntegratedCons.txt'
    text2 = 'IntegratedPros.txt'
    # test = 'test.txt'
    positive = 'positive-words.txt'
    negative = 'negative-words.txt'
    positivewords = readsentiment(positive)         #read the positive word list
    negativewords = readsentiment(negative)         #read the negative word list
    readtext(text1, positivewords, negativewords)      #first time run without negation operations.
    readtext(text2, positivewords, negativewords)      #first time run without negation operations.
    readtext_negation(text1, positivewords, negativewords)         #second time run with negation operations.
    readtext_negation(text2, positivewords, negativewords)         #second time run with negation operations.
    # readtext(test, positivewords, negativewords)
    # readtext_negation(test, positivewords, negativewords)





