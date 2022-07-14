# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

from operator import xor
import sDES
import time
import codecs
import filter
import random
from textwrap import wrap

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
t_start = time.process_time()

# convert cypher text string into a byte array; CONSTANT FOR ALL ITERATIONS
cipherbytes = bytearray(test.ciphertext, 'utf-8')
print(cipherbytes)
# bytes/bytes in cypher
cipher_byte_length = len(test.ciphertext)
cipher_bit_length = cipher_byte_length*8

# initalize filter
destination = 'filtered_bruteforceresults_compare.txt'
# only save results that contain at least 75% plaintext
minlength = 0.75
# apply filter
textfilter = filter.filter(destination, rule, int((len(test.ciphertext)*minlength)))


# randoms seed
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
#decrypt error cyphertext
for x in range(0, 2**cipher_bit_length):
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

# textfilter.fileclose()
t_stop = time.process_time()
print('Elapsed Time: ', t_stop-t_start, 's')