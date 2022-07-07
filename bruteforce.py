# code to brute force simplified DES ciphertext
# Joseph Garro and Savannah Rimmele

import sDES
import time
import codecs
import filter

key = 0x0AA
plaintext = "Dr. Tran, Look at all of our progress! We can try adding in an error to this now!"
IV = 0x52

print(bytes(plaintext, 'utf-8'))
test = sDES.sDES(key, plaintext, IV)
print(test.encrypt())
print(test.decrypt(key, IV))

# regular expression to find desirable plaintexts
# rule to finlter non prinatable ascii
rule = r"[^a-zA-Z0-9 -~]+"

# timer
# Using process_time returns float of the sum of the system and user CPU time of current process (Excludes time elapsed during sleep & is process wide)
t_start = time.process_time()

# initalize filter
destination = 'filtered_bruteforceresults.txt'
textfilter = filter.filter(destination, rule, 40)

# write cyphertext to output
textfilter.printcyphertext("no error")

# try all possible key values
for i in range(0, 1023):
     decryptRes = test.decrypt(i, IV)
     # call the parser
     #print(str(decryptRes.encode('ascii', errors='ignore')))
     #textfilter.filterinput(decryptRes.encode('ascii', errors='ignore'), i)
     textfilter.filterinput(decryptRes.encode('ascii', errors='ignore'), i)

textfilter.fileclose()
t_stop = time.process_time()
print('Elapsed Time: ', t_stop-t_start, 's')

# xor cyphertext with errors
#   trying ciphertext with keys
# parser
# final text file
# end timer
#
