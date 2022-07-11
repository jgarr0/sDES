# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

import sDES
import time
import codecs
import filter
from textwrap import wrap

key = 0x0AA
plaintext = "Dr. Tran, Look at all of our progress! We can try adding in an error to this now!"
#plaintext = "test"
IV = 0x52

print(bytes(plaintext, 'ascii'))
test = sDES.sDES(key, plaintext, IV)
print(test.encrypt())
print(test.ciphertext)
print(test.decrypt(key, IV))

# regular expression to find desirable plaintexts
# rule to finlter non prinatable ascii
rule = r"[^a-zA-Z0-9 -~]+"

# timer
# Using process_time returns float of the sum of the system and user CPU time of current process (Excludes time elapsed during sleep & is process wide)
t_start = time.process_time()

# convert cypher text string into a byte array; CONSTANT FOR ALL ITERATIONS
cipherbytes = bytearray(test.ciphertext, 'utf-8')
# bytes/bytes in cypher
cipher_byte_length = len(test.ciphertext)
cipher_bit_length = cipher_byte_length*8

# initalize filter
destination = 'filtered_bruteforceresults.txt'
#textfilter = filter.filter(destination, rule, int(cipher_byte_length/2))
textfilter = filter.filter(destination, rule, int((len(test.ciphertext)*0.75)))

# begin introducing error
for x in range(0, (2**cipher_bit_length)):
     # make copy of original bytes
     tempbytes = cipherbytes
     # integer value of error, will increase from 1 -> 2^N - 1
     errorvalue = bin(x)[2:].zfill(cipher_byte_length * 8)
     # print error value
     #print(errorvalue)
     #  break integer into an error for each byte
     xor_values = wrap(errorvalue[2:], 8)
     # xor each bytes error with original bytes
     index = 0
     for z in range(0, cipher_byte_length):
          # XOR
          tempbytes[index] = cipherbytes[index] ^ int(xor_values[index], base=2)
          # update index
          index+=1

     # form new ciphertext
     error_ciphertext = bytes(tempbytes)
     # reassign ciphertext to new value
     test.ciphertext = error_ciphertext.decode('utf-8', errors='ignore')
     # write cyphertext to output
     textfilter.printcyphertexterror(str(x))

     # try all possible key values
     for i in range(0, 1023):
          decryptRes = test.decrypt(i, IV)
          #call the parser
          #textfilter.filterinput(decryptRes.encode('ascii', errors='ignore'), i)
          textfilter.filterinput(decryptRes.encode('utf-8'), i)

textfilter.fileclose()
t_stop = time.process_time()
print('Elapsed Time: ', t_stop-t_start, 's')

# xor cyphertext with errors
#   trying ciphertext with keys
# parser
# final text file
# end timer
#
