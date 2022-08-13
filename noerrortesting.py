import sDES
# code to brute force a specified number of errors applied to ciphertext
# Joseph Garro and Savannah Rimmele

from operator import xor
from sys import byteorder
import sDES
import time
import filter
import random
import codecs
import multiprocessing as mp
import os

#--------------------------------------------------------------
# GLOBAL VARIABLES
# NUM_ERRORS = 3
# rule to filter non prinatable ascii
RULE = r"[^a-zA-Z0-9 -~]+"
#--------------------------------------------------------------

# main function
def test(_KEY, _PLAINTEXT, _IV):

    # initialize SDES
    key = _KEY
    plaintext = _PLAINTEXT
    IV = _IV

    test = sDES.sDES(key, plaintext, IV)
    test.encrypt()
    print("---------------------------------------------------------------")
    print("plaintext:  ", plaintext)
    print("ciphertext: ", test.ciphertext)
    print("---------------------------------------------------------------")
    # get length of ciphertext
    ciphertextlength = len(test.ciphertext)

    # grab numerical value of ciphertext bytes
    ciphertext_int = []
    for i in range(0, ciphertextlength):
        ciphertext_int.append(ord(test.ciphertext[i]) << 8*((ciphertextlength-1)-i))

    print("int values for each byte: ", ciphertext_int)   
    # sum ciphertext = n bit number, n is the size of the ciphertext
    totalciphertext = sum(ciphertext_int)
    print("total ciphertext: ", totalciphertext)
    print("begin bruteforcing")

    # timer
    t_start = time.perf_counter()

    # check if results directory exists
    dir1 = "./results/"
    direxist1 = os.path.exists(dir1)

    # create directory for results if nonexistant
    if not direxist1:
        try:
            os.mkdir(dir1)
        except OSError as error:
            print(error) 

    # check if results directory exists
    dir2 = "./results/no_error_brute_results_{}".format(plaintext)
    direxist2 = os.path.exists(dir2)

    # create directory for results if nonexistant
    if not direxist2:
        try:
            os.mkdir(dir2)
        except OSError as error:
            print(error)

    # initalize filter
    destination = '{}/filtered_bruteforceresults_no_error.txt'.format(dir2)
    # only save results that contain at least 75% plaintext
    minlength = 0
    # apply filter
    textfilter = filter.filter(destination, RULE, int(ciphertextlength*minlength))

    # dummy SDES instance
    decryptattempt = sDES.sDES(0x000, "", IV)
    # decrypt SDES
    decryptattempt.ciphertext = test.ciphertext
    # try all possible key values
    for i in range(0, 1024):
        textfilter.filterinput(decryptattempt.decrypt(i, IV), i)

    t_stop = time.perf_counter()
    totaltime = t_stop-t_start
    print('Elapsed Time: ', t_stop-t_start, 's')
    return totaltime
