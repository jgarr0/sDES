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
#NUM_ERRORS = 3
# rule to filter non prinatable ascii
RULE = r"[^a-zA-Z0-9 -~]+"
#--------------------------------------------------------------

# generate a random bit of error out of n bits
def errorgen(n):
    # random leftshift from 0 to 7 places
    leftshiftn = random.randint(0, n-1)
    return (1 << leftshiftn)

def multicore_decrypt(dir, errorbytes, length, rule, IV, start, end, corrections):
    try:
        cipherbytes = errorbytes
        print("process cipher bytes: ", errorbytes)
        # grab numerical value of ciphertext bytes
        sumcipherbytes = []
        for i in range(0, length):
            sumcipherbytes.append(cipherbytes[i] << 8*((length-1)-i))
        # sum bytes
        sumcipherbytes = sum(sumcipherbytes)
        
        # initalize filter
        destination = '{}/filtered_bruteforceresults_{}_{}.txt'.format(dir, start, end)
        # only save results that contain at least 75% plaintext
        minlength = 0.75
        # apply filter
        textfilter = filter.filter(destination, rule, int(length*minlength))

        # decrypt error cyphertext
        for x in range(0, len(corrections)):
            # create ciphertext with correction appplied
            errorcorrection = sumcipherbytes ^ int(corrections[x])
            # dummy SDES instance
            decryptattempt = sDES.sDES(0x000, "", IV)
            # decrypt SDES
            decryptattempt.ciphertext = errorcorrection.to_bytes(length, byteorder="big")
            # write cyphertext to output
            textfilter.printcyphertexterror(str(corrections[x]))
            # try all possible key values
            for i in range(0, 1024):
                textfilter.filterinput(decryptattempt.decrypt(i, IV), i)
        res = "errors {} - {} done".format(start, end)
        print(res)
        return
    except KeyboardInterrupt:
        return

# main function
def adderr(_KEY, _PLAINTEXT, _IV, _NUM_ERRORS):
    # initalize random seed
    random.seed()

    # initialize SDES
    key = _KEY
    plaintext = _PLAINTEXT
    IV = _IV

    test = sDES.sDES(key, plaintext, IV)
    test.encrypt()
    print("---------------------------------------------------------------")
    print("standard SDES encryption")
    print("plaintext:  ", plaintext)
    print("ciphertext: ", test.ciphertext)
    print("---------------------------------------------------------------")
    # get length of ciphertext
    ciphertextlength = len(test.ciphertext)

    # generate error
    errorvalues = set()
    # add values to set to prevent duplicate errors
    while(len(errorvalues) != _NUM_ERRORS):
        errorvalues.add(errorgen(8*ciphertextlength))
        # add a pause to try and prevent duplicate values
        time.sleep(random.randrange(0, 15, 1)/10)

    # grab numerical value of ciphertext bytes
    ciphertext_int = []
    for i in range(0, ciphertextlength):
        ciphertext_int.append(ord(test.ciphertext[i]) << 8*((ciphertextlength-1)-i))
    # sum ciphertext = n bit number, n is the size of the ciphertext
    totalciphertext = sum(ciphertext_int)

    # display ciphertext information
    print("ciphertext information:")
    print("int values for each byte: ", ciphertext_int)   
    print("total ciphertext: ", totalciphertext)

    # convert set to list
    errorvalues = list(errorvalues)
    # print error values
    # sum errors = n bit number, n is the size of the ciphertext
    totalerror = sum(errorvalues)

    # dispay information about errors
    print("\nerror information:")
    print("error values: ", errorvalues)
    print("total error: ", totalerror)

    # apply error to ciphertext
    errortext_int = totalciphertext ^ totalerror
    errortext_bytes = errortext_int.to_bytes(ciphertextlength, byteorder="big")

    # print ciphertext with error applied, invalid chars not displayed
    errortext = str(errortext_bytes, encoding="utf-8", errors="ignore")
    print("errortext: ", errortext)
    print("errortext bytes: ", errortext_bytes)
    print("---------------------------------------------------------------")
    # HAVE TO USE ERROR TEXT BYTES, AS CIPHERTEXT WITH ERRORS CAN BE INVALID
    print('\033[1m' + "must apply error correction to errortext bytes above. \nthe displayed 'errortext' is the errortext bytes cast to an utf-8\nencoded string. there is the potential for invalid utf characters\nto occur, which are not representative of the SDES encoded\nvalue nor the error value applied to it." + '\033[0m')
    print("---------------------------------------------------------------")
    print("begin error correction and bruteforcing")

    # timer
    t_start = time.perf_counter()

    # multicore decryption
    numcore = mp.cpu_count()

    # open dictionary automatically
    dict_size = 8*ciphertextlength
    fname = "./dictionaries/dictionary_{}_errors_{}_bits.txt".format(_NUM_ERRORS, dict_size)
    try:
        f = open(fname, 'r')
    except IOError:
        print("need to provide a dictionary consisting of error values to check called '{}'".format(fname))
        return

    # read in corrections + get number of corrections
    corrections = f.readlines()
    numcorrections = len(corrections)

    # strip newlines
    for i in range(0, numcorrections):
        corrections[i] = str.strip(corrections[i])

    # assign to single core if corections < core count
    corrected_values = []
    if(numcorrections < numcore):
        corrected_values.append(corrections[0:numcorrections])
    # otherwise, divide up work
    else:
        # assign work
        work = int(numcorrections/numcore)
        upperbounds = [0] * numcore
        lowerbounds = [0] * numcore
        for z in range(0, numcore):
            lowerbounds[z] = work*z
            upperbounds[z] = work*(z+1)
        # catch non-even powers of 2
        upperbounds[numcore-1] = numcorrections

        for i in range(0, numcore):
            corrected_values.append(corrections[lowerbounds[i]:upperbounds[i]])

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
    dir2 = "./results/{}_{}_dict_results".format(plaintext, _NUM_ERRORS)
    direxist2 = os.path.exists(dir2)

    # create directory for results if nonexistant
    if not direxist2:
        try:
            os.mkdir(dir2)
        except OSError as error:
            print(error)    

    # launch decryption method on each core
    with mp.Pool() as pool:
        try:
            pool.starmap(multicore_decrypt, [(dir2, errortext_bytes, ciphertextlength ,RULE, IV, corrected_values[i][0], corrected_values[i][len(corrected_values[i])-1], corrected_values[i]) for i in range(0, len(corrected_values))])
        except KeyboardInterrupt:
            print("killed pool of processes")
            pool.terminate()
        else:
            pool.close()
    pool.close()

    t_stop = time.perf_counter()
    totaltime = t_stop-t_start
    print('Elapsed Time: ', t_stop-t_start, 's')
    return totaltime

# start main process
#if __name__ == "__main__":
#    main()