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

#--------------------------------------------------------------
# GLOBAL VARIABLES
NUM_ERRORS = 3
# rule to filter non prinatable ascii
RULE = r"[^a-zA-Z0-9 -~]+"
#--------------------------------------------------------------

# generate a random bit of error out of n bits
def errorgen(n):
    # random leftshift from 0 to 7 places
    leftshiftn = random.randint(0, n-1)
    return (1 << leftshiftn)

def multicore_decrypt(errorbytes, length, rule, IV, start, end):
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
        destination = 'filtered_bruteforceresults_{}_{}.txt'.format(start, end)
        # only save results that contain at least 75% plaintext
        minlength = 0
        # apply filter
        textfilter = filter.filter(destination, rule, int(length*minlength))

        # decrypt error cyphertext
        for x in range(start, end):
            # create ciphertext with correction appplied
            errorcorrection = sumcipherbytes ^ x
            # dummy SDES instance
            decryptattempt = sDES.sDES(0x000, "", IV)
            # decrypt SDES
            decryptattempt.ciphertext = errorcorrection.to_bytes(length, byteorder="big")
            # write cyphertext to output
            textfilter.printcyphertexterror(str(x))
            # try all possible key values
            for i in range(0, 1024):
                textfilter.filterinput(decryptattempt.decrypt(i, IV), i)
    except KeyboardInterrupt:
        return

# main function
def main():
    # initalize random seed
    random.seed()

    # initialize SDES
    key = 0x2ac
    plaintext = "hi"
    IV = 0x93
    test = sDES.sDES(key, plaintext, IV)
    test.encrypt()
    print("---------------------------------------------------------------")
    print("plaintext:  ", plaintext)
    print("ciphertext: ", test.ciphertext)
    print("---------------------------------------------------------------")
    # get length of ciphertext
    ciphertextlength = len(test.ciphertext)

    # generate error
    errorvalues = set()
    # add values to set to prevent duplicate errors
    while(len(errorvalues) != NUM_ERRORS):
        errorvalues.add(errorgen(8*ciphertextlength))
        # add a pause to try and prevent duplicate values
        time.sleep(random.randrange(0, 15, 1)/10)

    # convert set to list
    errorvalues = list(errorvalues)
    # print error values
    print("error values: ", errorvalues)
    # sum errors = n bit number, n is the size of the ciphertext
    totalerror = sum(errorvalues)
    print("total error: ", totalerror)

    # grab numerical value of ciphertext bytes
    ciphertext_int = []
    for i in range(0, ciphertextlength):
        ciphertext_int.append(ord(test.ciphertext[i]) << 8*((ciphertextlength-1)-i))

    print("int values for each byte: ", ciphertext_int)   
    # sum ciphertext = n bit number, n is the size of the ciphertext
    totalciphertext = sum(ciphertext_int)
    print("total ciphertext: ", totalciphertext)

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

    # divide permutations of ciphertext betwen cores
    totalpermutations = 2**(8*ciphertextlength)
    work = int(totalpermutations/numcore)
    # assign work
    upperbounds = [0] * numcore
    lowerbounds = [0] * numcore
    for z in range(0, numcore):
        lowerbounds[z] = work*z
        upperbounds[z] = work*(z+1)
    # catch non-even powers of 2
    upperbounds[numcore-1] = totalpermutations-1

    # launch decryption method on each core
    with mp.Pool() as pool:
        try:
            pool.starmap(multicore_decrypt, [(errortext_bytes, ciphertextlength ,RULE, IV, lowerbounds[i], upperbounds[i]) for i in range(0, numcore)])
        except KeyboardInterrupt:
            print("killed pool of processes")
            pool.terminate()
        else:
            pool.close()

    # textfilter.fileclose()
    t_stop = time.perf_counter()
    print('Elapsed Time: ', t_stop-t_start, 's')

# start main process
if __name__ == "__main__":
    main()