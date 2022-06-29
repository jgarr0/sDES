# implementation of simplified DES (sDES)
# Joseph Garro and Savannah Rimmele

import math

class sDES:

    # constants
    #############################################################
    # permutation tables to generate subkeys
    P10_T = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8_T = [6, 3, 7, 4, 8, 5, 10, 9]

    # Initial Permutation
    IP = [2, 6, 3, 1, 4, 8, 5, 7]

    # Final Permutation
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]

    # Expansion Permutation
    E = [4, 1, 2, 3, 2, 3, 4, 1]

    # Substitution Boxes
    S0 = [[1, 0, 3, 2],
        [3, 2, 1, 0], 
        [0, 2, 1, 3], 
        [3, 1, 3, 2]]

    S1 = [[0, 1, 2, 3], 
        [2, 0, 1, 3], 
        [3, 0, 1, 0], 
        [2, 1, 0, 3]]

    # Apply P4 Permutation to the S-Box output
    P4 = [2, 4, 3, 1]


    # instance vars
    #############################################################
    K1 = ""
    K2 = ""
    key = ""
    plaintext = ""
    cyphertext = ""

    def __init__(self, input_key = "", input_plaintext = ""):
        self.key = input_key & 0x3FF
        self.plaintext = input_plaintext & 0xFF

    def circularLeftShift(self, input):
        numbits = len(input)
        max = int(math.pow(2, numbits)-1)
        addme = int(0x000)
        if(input[0] == '1'):
            addme = int(0x001)
        # left shift
        temp_input = int(input, 2) << 1
        # truncate shift to original size
        temp_input = temp_input & max
        # wrap around leading bit
        temp_input = temp_input | addme
        return temp_input

    def permutate(self, input, dictionary, length=10):
        temp = ""
        input_copy = list(bin(input)[2:].zfill(length))
        for i in range(0, len(dictionary)):
            temp += input_copy[dictionary[i]-1]
        return "".join(temp)

    # function definitions
    def deriveKeys(self):                   # 2^10
        # form P10
        TMP_P10 = self.permutate(self.key, self.P10_T)
        L_P10 = self.circularLeftShift(TMP_P10[0:5])
        print("L_P10:", bin(L_P10)[2:].zfill(5))
        R_P10 = self.circularLeftShift(TMP_P10[5:])
        print("R_P10:", bin(R_P10)[2:].zfill(5))

        # combine right and left
        P10 = (0x3FF & (L_P10 << 5) )| R_P10

        # form K1
        #P10_LST = bin(P10)[2:].zfill(10)
        #print("P10_LST: ", P10_LST)

        # Permutate P10_LST with P8 to derive the first key 
        self.K1 = self.permutate(P10, self.P8_T)
        print("First Key: ", self.K1)

        L3_P10 = self.circularLeftShift(bin(self.circularLeftShift(bin(L_P10)[2:].zfill(5)))[2:].zfill(5))
        print("L3_P10: ", bin(L3_P10)[2:].zfill(5))
        R3_P10 = self.circularLeftShift(bin(self.circularLeftShift(bin(R_P10)[2:].zfill(5)))[2:].zfill(5))
        print("R3_P10: ", bin(R3_P10)[2:].zfill(5))

        # form k2
        P8 = (0x3FF & (L3_P10 << 5) )| R3_P10
        #P8_LST = bin(P8)[2:].zfill(10)

        # Permutate to derive the second key 
        self.K2 = self.permutate(P8, self.P8_T)
        print("Second Key: ", self.K2)

    def encrypt(self):
        permuted_input = self.permutate(self.plaintext, self.IP, 8)
        

# main
key = 0x282                             # 10 bit key
plaintext = 0xF3                        #  8 bit plaintext

test = sDES(key, plaintext)
print(hex(test.key))
test.deriveKeys() 
test.encrypt()