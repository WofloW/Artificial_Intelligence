import cPickle as pickle
import argparse

### read in data from an ARFF file and return the following data structures:
### A attr that maps an attribute index to a attrionary mapping attribute names to either:
###    - possible values
###    - the string 'string'
###    - the string 'numeric'
### A list containing all data instances, with each instance stored as a tuple.
def readArff(filehandle) :
    attr={}
    num_attr=1
    line = filehandle.readline()
#   readARFF attribute
    data =[]
    data_flag = False
    while line:
        if '@attribute' in line:
            start = 0
            first_flag = True
            for i in range(len(line)):
                if line[i] == '{':

                    start = i+1
                if line[i] == ',':

                    if line[i+1] != ' ':
                        if first_flag:
                            attr[num_attr] ={line.split()[1]:[line[start:i]]}
                            first_flag= False
                        else:
                            attr[num_attr][line.split()[1]] +=[line[start:i]]
                    else:
                        if first_flag:
                            attr[num_attr] ={line.split()[1]:[line[start:i]]}
                            first_flag= False
                        else:
                            attr[num_attr][line.split()[1]] +=[line[start+1:i]]

                    start = i+1
                if line[i] == '}':
                    if line[start] != ' ':
                        attr[num_attr][line.split()[1]] +=[line[start:i]]
                    else:
                        attr[num_attr][line.split()[1]] +=[line[start+1:i]]
            num_attr += 1
        line = filehandle.readline()


        if '@data' in line:
            data_flag = True
            line = filehandle.readline()
        if data_flag:
            if '\n' in line:
                data.append(tuple(line[:-1].split(',')))
            else:
                data.append(tuple(line.split(',')))

#    print attr
#    print data
    return attr,data




### Compute ZeroR - that is, the most common data classification without 
### examining any of the attributes. Return the most common classification.
def computeZeroR(attributes, data) :
    sum_yes = 0
    for i in data:
        if i[-1]=='yes':
            sum_yes +=1
    print 'sum_yes:'+str(sum_yes)



### Usage: readARFF {--pfile=outfile} infile
### If --pfile=outfile, pickle and store the results in outfile. Otherwise, 
### print them to standard out. Your code should also call computeZeroR and 
### print out the results.

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='''function that can read in an ARFF file and generate the following data structures''')
    parser.add_argument('--pfile', type=argparse.FileType('w'), help='''the name of a file to use as output''')
    parser.add_argument('file', type=argparse.FileType('r'), help='''the name of a file to use as input''')
    args = parser.parse_args()
    attr,data=readArff(args.file)

    if args.pfile:
        args.pfile.write(str(attr))
        args.pfile.write(str(data))
        args.pfile.close()
    else:
        print 'attribute:'
        print attr
        print 'data:'
        print data
    computeZeroR(attr,data)
    



