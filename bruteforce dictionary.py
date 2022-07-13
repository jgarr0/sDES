# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

import sDES
import time
import codecs
import filter
from textwrap import wrap

# initialize SDES
key = 0x0AA
plaintext = "test"
IV = 0x52
test = sDES.sDES(key, plaintext, IV)
test.encrypt()

# regular expression to find desirable plaintexts
# rule to finlter non prinatable ascii
rule = r"[^a-zA-Z0-9 -~]+"

# timer
# Using process_time returns float of the sum of the system and user CPU time of current process (Excludes time elapsed during sleep & is process wide)
t_start = time.process_time()

# convert cypher text string into a byte array; CONSTANT FOR ALL ITERATIONS
cipherbytes = bytearray(test.ciphertext, 'utf-8')
print(cipherbytes)
# bytes/bytes in cypher
cipher_byte_length = len(test.ciphertext)
print(cipher_byte_length)
cipher_bit_length = cipher_byte_length*8

# initalize filter
destination = 'filtered_bruteforceresults_fromdict.txt'
# only save results that contain at least 75% plaintext
minlength = 0.75
# apply filter
textfilter = filter.filter(destination, rule, int((len(test.ciphertext)*minlength)))

dict = open("dictionary.txt", "r")

# begin introducing error
for x in dict:
     # make copy of original bytes
     tempbytes = cipherbytes
     # integer value of error, will increase from 1 -> 2^N - 1
     errorvalue = bin(int(x))[2:].zfill(cipher_byte_length * 8)
     print(errorvalue)
     #  break integer into an error for each byte
     xor_values = wrap(errorvalue, 8)
     print(xor_values)
     # xor each bytes error with original bytes
     for z in range(0, cipher_byte_length):
          print("old: ", tempbytes[z])
          tempbytes[z] = cipherbytes[z] ^ int(xor_values[z], base=2)
          print("new: ", tempbytes[z])


     # form new ciphertext
     error_ciphertext = bytes(tempbytes)
     # reassign ciphertext to new value
     test.ciphertext = error_ciphertext.decode('utf-8', errors='ignore')
     # write cyphertext to output
     textfilter.printcyphertexterror(str(x))

     # try all possible key values
     for i in range(0, 1023):
          decryptRes = test.decrypt(i, IV)
          textfilter.filterinput(decryptRes.encode('utf-8'), i)

textfilter.fileclose()
t_stop = time.process_time()
print('Elapsed Time: ', t_stop-t_start, 's')