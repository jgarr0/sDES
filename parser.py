# parser to analyze brute forced sDES plaintexts
# Joseph Garro and Savannah Rimmele

import re

class parser:
    # save path to text file
    PATH = ""

    def __init__(self, filepath):
        self.PATH = filepath
    
    def parse(self):
        # do not parse if no file loaded
        if not self.PATH:
            print("You need to provide a file to parse")
            return
        # otherwise parse
        else:
            # load file
            ptlist = open(self.PATH, 'rb')
            # parse one line at a time
            #for x in ptlist:
            #    print(x.decode())
            x = ptlist.readlines()[169]
            print(x.decode('ascii'))
            print("\n")
            print(ord(x))
            #print(str(x[2:].decode()))
            #close file
            ptlist.close()

test = parser("bruteforceresults.txt")
test.parse()