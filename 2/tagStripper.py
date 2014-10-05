
import re, getopt, sys, urllib
# No other modules should be imported besides the above

### This method should use the re module to remove all HTML tags from
### an input string. You may assume that anything
### between a '<' and a '>' is a tag.
### For example, inputting the string "<h2>here is some stuff</h2>"
### should return "here is some stuff"
def regexStrip(instring) :
    p = re.sub("<[^>]*>","",instring)
    if p:
        return p
    else:
        return 'No match'

### This method should remove HTML tags "by hand"; that is, by
### iterating through the string without using the re module.
### It should have the same behavior as regexStrip.
def handStrip(instring):
    tag_flag = [False]
    def check_flag(i):
        if tag_flag[0]:
            tag_flag[0] = (i != '>')
            return False
        elif (i == '<'):
            tag_flag[0] = True;
            return False
        return True
    return ''.join(i for i in instring if check_flag(i))

### here is a main for you to use. It demonstrates both the use of the
### getopt module and also exception handling. You shouldn't need to
### change it.

if __name__ == '__main__' :
    try :
        options, args = getopt.getopt(sys.argv[1:], 'rh')
    except getopt.GetoptError :
        print 'Usage: tagstripper.py {-r|-h} URL'
        sys.exit(0)

    try :
        if options and '-r' in options[0] :
            print regexStrip(urllib.urlopen(args[0]).read())
        else :
            print handStrip(urllib.urlopen(args[0]).read())
    except IOError :
        print 'Unable to open ' + args[0]
        sys.exit(0)


