from itertools import permutations
from math import perm
import os   

# parameters for maximum ciphertext size (bits) and number of errors
MAX_LENGTH = 64
MAX_ERROR = 6

# modified recursion from https://stackoverflow.com/questions/64890117/what-is-the-best-way-to-generate-all-binary-strings-of-the-given-length-in-pytho
def generator(f, length, numerror, bin = ""):
    if(len(bin) == length):
        if(bin.count('1') < numerror+1):
            f.write(str(int(bin, base=2)) + "\n")
    else:
        generator(f, length, numerror, bin + '0')
        generator(f, length, numerror, bin + '1')

def main():
    # check if dictionaries directory exists
    direxist = os.path.exists("./dictionaries")

    # create directory for dictionaries if nonexistant
    if not direxist:
        try:
            os.mkdir("./dictionaries")
        except OSError as error:
            print(error)     

    for i in range(8, MAX_LENGTH+8, 8):
        for j  in range(1, MAX_ERROR+1):
            # auto select dictionary for future cases
            fname = "./dictionaries/dictionary_{}_errors_{}_bits.txt".format(j, i)
            # write dictionary if it does not exist
            dictexist = os.path.exists(fname)
            if not dictexist:
                try:
                    f = open(fname, "x",)
                except OSError as error:
                    print(error)    
                else:    
                    generator(f, i, j)
                    print("successfully created " + fname)

# start main process
if __name__ == "__main__":
    main()