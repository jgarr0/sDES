# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

import sDES
import time

key = 0x0AA
plaintext = "Dr. Tran, Look at all of our progress! We can try adding in an error to this now!"
IV = 0x52

bruteforceresults = open("bruteforceresults.txt", 'w')

print(bytes(plaintext, 'utf-8'))
test = sDES.sDES(key, plaintext, IV)
print(test.encrypt())
print(test.decrypt(key, IV))
# timer
# Using perf_counter returns value of performance counter with highest available res. (Includes time elapsed during sleep & is system wide)
t_start = time.perf_counter()
for i in range(0, 1024):
     decryptRes = test.decrypt(i, IV)
     bruteforceresults.write(str(decryptRes.encode('utf-8', errors='replace')) + "\n")
     #if(decryptRes == plaintext):
     #    bruteforceresults.write("\titeration: " + repr(i) +  "matches\n")

# call the parser

t_stop = time.perf_counter()
print('Elapsed Time: ', t_stop-t_start, 's')

# xor cyphertext with errors
#   trying ciphertext with keys
# parser
# final text file
# end timer
#
