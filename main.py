# implementation of simplified DES (sDES)
# Joseph Garro and Savannah Rimmele

import sDES
import re

# sample program to create an SDES cyphertext for a given input
# regex expression taken from https://www.geeksforgeeks.org/how-to-validate-hexadecimal-color-code-using-regular-expression/#:~:text=regex%20%3D%20%22%5E%23(%5BA%2D,with%20a%20'%23'%20symbol.
# and https://stackoverflow.com/questions/9221362/regular-expression-for-a-hexadecimal-number

while(1):
    # get input text
    input_string = input("Input any size plaintext to encrypt: ")
    # get input key
    input_key = input("Input a 10 bit key as a hex value (Ex 0x33D): ")
    # regex expression to ensure that key is valid ()
    while not re.match("^(?:0[xX])?([0-9a-fA-F]{3})$", input_key):
        input_key = input('Only hex values with 3 digits are allowed: ')
    input_key = int(input_key, 16)
    # empty IV to select proper mode of SDES
    input_iv = ""
    # if input > 8 bits, need initialization vector for CBC
    if len(input_string) > 1:
        input_iv = input("Input an 8 bit initialization vector as a hex value (Ex 0x4C): ")
        while not re.match("^(?:0[xX])?([0-9a-fA-F]{2})$", input_iv):
            input_iv = input('Only hex values with 2 digits are allowed: ')
    # convert to int
    if input_iv:
        input_iv = int(input_iv, 16)
    # encrypt with sDES using passed values
    # create new sDES object with CBC if IV is not null
    if input_iv:
        encryptme = sDES.sDES(input_key, input_string, input_iv)
        # if CBC is not enabled
    else:
        encryptme = sDES.sDES(input_key, input_string)

    # encrypt input + display ciphertext
    print("Ciphertext: ", encryptme.encrypt())

    # input for this example is known; allow decryption until input achieved
    print("Input has now been encrypted. Input keys until the cyphertext is decrypted successfully")
    decrypt_result = ""
    while(decrypt_result != input_string):
        guess_key = input("Input a 10 bit key as a hex value (Ex 0x33D): ")
        # regex expression to ensure that key is valid ()
        while not re.match("^(?:0[xX])?([0-9a-fA-F]{3})$", guess_key):
            guess_key = input('Only hex values with 3 digits are allowed: ')
        guess_key = int(guess_key, 16)
        # attempt to decrypt with provided key
        decrypt_result = encryptme.decrypt(guess_key, input_iv)
        print("Plaintext: ", decrypt_result)
    print('\n')