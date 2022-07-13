# filter to sort brute forced sDES plaintexts
# Joseph Garro and Savannah Rimmele

import codecs
import re

class filter:
    # save path to text file
    FILE = ""
    RULE = ""
    MIN_LENGTH = ""

    def __init__(self, file, rule, min_length):
        self.FILE = codecs.open(file, "w", encoding='utf-8')
        self.RULE = rule
        self.MIN_LENGTH = min_length

    def printcyphertexterror(self, text):
        self.FILE.write("cyphertext error: " + text + "\n")

    def filterinput(self, text, key):
        newtext = re.sub(self.RULE, "", text.decode('utf-8'))
        if(len(newtext) >= int(self.MIN_LENGTH) and newtext == "do"):
            self.FILE.write("\tkey:" + "0x{:03x}".format(key) + "\tplaintext: " + str(newtext) + "\n")
    
    def fileclose(self):
        self.FILE.close()