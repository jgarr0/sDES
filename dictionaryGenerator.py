from itertools import permutations
from math import perm
import os   
import multiprocessing as mp
# parameters for maximum ciphertext size (bytes) and number of errors
MAX_LENGTH = 3
MAX_ERROR = 4

# generate files
def filegen(err, len):
    # auto select dictionary for future cases
    fname = "./dictionaries/dictionary_{}_errors_{}_bits.txt".format(err, len)
    #write dictionary if it does not exist
    dictexist = os.path.exists(fname)
    if not dictexist:
        try:
            f = open(fname, "x",)
        except OSError as error:
            print(error)    
        else:    
            generator(f, err, len)
            print("successfully created " + fname)

# modified recursion from https://stackoverflow.com/questions/64890117/what-is-the-best-way-to-generate-all-binary-strings-of-the-given-length-in-pytho
def generator(f, numerror, length, bin = ""):

    if(len(bin) == length):
        if(bin.count('1') < numerror+1):
            f.write(str(int(bin, base=2)) + "\n")
    else:
        generator(f, numerror, length, bin + '0')
        generator(f, numerror, length, bin + '1')

def main():
    # check if dictionaries directory exists
    direxist = os.path.exists("./dictionaries")

    # create directory for dictionaries if nonexistant
    if not direxist:
        try:
            os.mkdir("./dictionaries")
        except OSError as error:
            print(error)     

    # lists for error and length
    err = []
    len = []

    # create length values
    for i in range(1, MAX_LENGTH+1):
        len.append(int(8*i))

    # create error values
    for i in range(1, MAX_ERROR+1):
        err.append(i)
    
    #print([(err[i], len[j])for i in range(0, MAX_ERROR)for j in range(0, MAX_LENGTH)])
    with mp.Pool() as pool:
        try:
            pool.starmap(filegen, [(err[i], len[j])for i in range(0, MAX_ERROR)for j in range(0, MAX_LENGTH)])
        except KeyboardInterrupt:
            print("killed pool of processes")
            pool.terminate()
        else:
            pool.close()
    pool.close()
    return


# start main process
if __name__ == "__main__":
    main()