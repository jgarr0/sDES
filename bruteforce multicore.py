# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

from operator import xor
import sDES
import time
import codecs
import filter
import random
from textwrap import wrap
# multiprocessing
import multiprocessing as mp

def multicore_decrypt(sdesobj, rule, IV, start, end):
     cipherbytes = bytearray(sdesobj.ciphertext, 'utf-8')
     print(cipherbytes)
     # bytes/bytes in cypher
     cipher_byte_length = len(sdesobj.ciphertext)
     cipher_bit_length = cipher_byte_length*8

     # initalize filter
     destination = 'filtered_bruteforceresults_{}_{}.txt'.format(start, end)
     # only save results that contain at least 75% plaintext
     minlength = 0.75
     # apply filter
     textfilter = filter.filter(destination, rule, int((len(sdesobj.ciphertext)*minlength)))

     # decrypt error cyphertext
     for x in range(start, end+1):
          # save ciphertext
          cipherbackup = cipherbytes
          errorvalue = bin(int(x))[2:].zfill(cipher_byte_length * 8)
          #print("ERROR VALUE: ", errorvalue)
          #  break integer into an error for each byte
          xor_values = wrap(errorvalue, 8)

          # xor each bytes error with original bytes
          for z in range(0, cipher_byte_length):
               cipherbackup[z] = cipherbytes[z] ^ int(xor_values[z], base=2)

          # form test ciphertext
          error_ciphertext = bytes(cipherbackup)    

          decryptattempt = sDES.sDES(0x000, "", IV)
          decryptattempt.ciphertext = error_ciphertext.decode('utf-8', errors='ignore')

          # write cyphertext to output
          textfilter.printcyphertexterror(str(x))

          # try all possible key values
          for i in range(0, 1023):
               textfilter.filterinput((decryptattempt.decrypt(i, IV)).encode('utf-8'), i)

# main function
def main():
     # initialize SDES
     key = 0x2D6
     plaintext = "hi"
     IV = 0x93
     test = sDES.sDES(key, plaintext, IV)
     test.encrypt()

     # regular expression to find desirable plaintexts
     # rule to finlter non prinatable ascii
     rule = r"[^a-zA-Z0-9 -~]+"

     # timer
     # Using process_time returns float of the sum of the system and user CPU time of current process (Excludes time elapsed during sleep & is process wide)
     t_start = time.perf_counter()

     # convert cypher text string into a byte array; CONSTANT FOR ALL ITERATIONS
     cipherbytes = bytearray(test.ciphertext, 'utf-8')
     print(cipherbytes)
     # bytes/bytes in cypher
     cipher_byte_length = len(test.ciphertext)
     cipher_bit_length = cipher_byte_length*8

     # random seed
     random.seed()

     # begin introducing error
     tempbytes = cipherbytes
     print(tempbytes)
     for z in range(0, cipher_byte_length):
          # xor each ciphertext byte with 0-255
          tempbytes[z] = cipherbytes[z] ^ random.randint(0, 255)

     # form new ciphertext
     print("BYTES WITH ERROR: ",tempbytes)
     error_ciphertext = bytes(tempbytes)
     print("PLAINTEXT ERROR:  ",error_ciphertext)
     test.ciphertext = error_ciphertext.decode('utf-8', errors='ignore')

     # convert cypher text string into a byte array; CONSTANT FOR ALL ITERATIONS
     cipherbytes = bytearray(test.ciphertext, 'utf-8')
     print(test.decrypt(0x13F, IV))

     # multicore decryption
     numcore = mp.cpu_count()

     # divide permutations of ciphertext betwen cores
     totalpermutations = 2**cipher_bit_length
     work = int(totalpermutations/numcore)

     # assign work
     upperbounds = [0] * numcore
     lowerbounds = [0] * numcore
     for z in range(0, numcore):
          lowerbounds[z] = work*z
          upperbounds[z] = work*(z+1)

     # launch decryption method on each core
     with mp.Pool() as pool:
          pool.starmap(multicore_decrypt, [(test, rule, IV, lowerbounds[i], upperbounds[i]) for i in range(0, numcore)])

     # textfilter.fileclose()
     t_stop = time.perf_counter()
     print('Elapsed Time: ', t_stop-t_start, 's')

# start main process
if __name__ == "__main__":
     main()