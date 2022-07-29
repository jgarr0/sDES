from itertools import permutations
import sDES
import re

d = ",.!?/&-:;@'...( "

def main():
    # initialize SDES
    key = 0x21F
    plaintext = "sav"
    IV = 0x93
    test = sDES.sDES(key, plaintext, IV)
    test.encrypt()
    value = '00000011' 
    print('Ciphertext: ', test.ciphertext)
    combinations = str(set(permutations( value, len(value))))
    #filtered = re.sub(",","",combinations)
    filtered = ' '.join(w for w in re.split("["+"\\".join(d)+"]", combinations) if w).replace(" ", "").replace(")", " ")
    print('Combinations: ', filtered, base=10)
    print('TYPE: ', type(filtered))


# start main process
if __name__ == "__main__":
    main()

#  íL/ -> has n errors
# Lí/ -> Doesnt help

# byte array, permutate (Bin)


# n errors, n =2
# 000000000000000000000000
# 100000000000000000000001
# 000000001100000000000000


# 0-(2^24)-1
# check combinations of 24c(number of errors)

# create a dictionary containing corrections for error that are applied to ciphertext
# if we know there are n bits in error, we have length choose n possible locatins of the error
# apply each correction to the ciphertext to "fix" the error, then brute force the resulting ciphertext
# instead of applying corrections ranging from 0 -> 2^length-1, applying corrections that only contain n '1's in them
# pull values from this dictionary to use as the correction; this means we ONLY try to fix n bit error
# 00000011 00001001
# 11111111 00001111

# 0110000111001111
# apply 2 buts of error -> 0110100111011111
#                          0000100000010000 -> value of error that we added

# 16c2 = 120; 00000000000011 <-> 1100000000000000 = 120 combinations
# apply corrections for 00000000000000 <-> 1111111111111111 = 65536 combinations

# So, we have binary sequence of len n. 00000...n -> 000...001, 000...010 
# Input error value 1-4: 
# 1 error: permuation (0000...001, length(n))
# 2 error: permuation( 000... 0011, lenght (n))

# remove quotes and comma inside parenthesis
# convert binary string to int, sort the ints, write ints to a file
#
# 3,5,6,9,10,12... for example 