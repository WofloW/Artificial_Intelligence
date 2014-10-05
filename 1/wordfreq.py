__author__ = 'wei fang'

import cPickle as pickle
#import pickle
import argparse
import string

### word frequencies:

### function that takes as input a string and, optionally,
### a dictionary, and returns the dictionary populated with word frequencies.
### provide options to strip punctuation and convert to lowercase.
##

### instr is the input string
### wf is an optional dictionary. This can be used to count over
### multiple files. If it is present, add counts to this.
### stripPunc and toLower indicate whether to strip punctuation and
### convert to lower case.
def wordfreq(instr, wf=None, stripPunc=True, toLower=True):
    dict1 = wf
    start = 0

###count num of each word
    for i in range(len(instr)):
        if instr[i] == ' ' or instr[i] == ',' or instr[i] == '.':
            if instr[start:i] == '':
                continue

            if instr[start:i] in dict:
                    dict1[instr[start:i]] += 1
            else:
                dict1[instr[start:i]] = 1
            start = i+1

        if i == len(instr)-1:
            if instr[start:i+1] == '':
                continue
            if instr[start:i+1] in dict:
                dict1[instr[start:i+1]] += 1
            else:
                dict1[instr[start:i+1]] = 1
            start = i+1
    print dict1

### strip punctuation
    if stripPunc:
        for j in instr:
            if j in string.punctuation:
                instr = instr.replace(j, "")

### convert to lower case
    if toLower:
        instr = instr.lower()
    print instr
    return dict1

### Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file
### if --nostrip, don't strip punctuation
### if --noConvert, don't convert everything to lower case
### if --pfile=outfile, pickle the resulting dictionary and store it in outfile.
### otherwise, print it to standard out.

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='function that gets the freq of word')

    parser.add_argument('--nostrip', action="store_false", help='''don't strip punctuation''')
    parser.add_argument('--noConvert', action="store_false", help='''don't convert everything to lower case''')
    parser.add_argument('--pfile', type=argparse.FileType('w'), help='''the name of a file to use as output''')
    parser.add_argument('file', type=argparse.FileType('r'), help='''the name of a file to use as input''')

#   debug: input in script
#   args = parser.parse_args(['--pfile', 'b.txt', 'a.txt'])
#   input by command-line arguments
    args = parser.parse_args()
    input = file.read(args.file)

    dict={}
#   debug: existing a dict
#   dict={'the': 1}

    dict2=wordfreq(input, dict, args.noConvert, args.nostrip)
    if args.pfile:
        pickle.dump(dict2, args.pfile)
    else:
        print dict2





