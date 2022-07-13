# program to create a simple sample dictionary

# length of desired ciphertext
from distutils.log import error


len_ciphertext = 112

# create dictionary text file
dictionary = open("dictionary.txt", "x")

# list for number of errors
#num_errors = [1, 2, 3, 4, 5, 6, 7, 8]
num_errors = [4]
error_values = set()

for x in num_errors:
    # if x == 1:
    #     for x1 in range(0, len_ciphertext):
    #         error_values.add(1 << x1)
    #     print("1 bit error done")
    # if x == 2:
    #     for x2 in range(0, len_ciphertext):
    #         for x3 in range(0, len_ciphertext):
    #             error_values.add(1 << x2 | 1 << x3)
    #     print("2 bit error done")
    # if x == 3:
    #     for x4 in range(0, len_ciphertext):
    #         for x5 in range(0, len_ciphertext):
    #             for x6 in range(0, len_ciphertext):
    #                 error_values.add(1 << x4 | 1 << x5 | 1 << x6)
    #     print("3 bit error done")
    if x == 4:
        for x7 in range(0, len_ciphertext):
            for x8 in range(0, len_ciphertext):
                for x9 in range(0, len_ciphertext):
                    for x10 in range(0, len_ciphertext):
                        error_values.add(1 << x7 | 1 << x8 | 1 << x9 | 1 << x10)
        print("4 bit error done")
    # if x == 5:
    #     for x11 in range(0, len_ciphertext):
    #         for x12 in range(0, len_ciphertext):
    #             for x13 in range(0, len_ciphertext):
    #                 for x14 in range(0, len_ciphertext):
    #                     for x15 in range(0, len_ciphertext):
    #                         error_values.add(1 << x11 | 1 << x12 | 1 << x13 | 1 << x14 | 1 << x15)
    #     print("5 bit error done")
    # if x == 6:
    #     for x16 in range(0, len_ciphertext):
    #         for x17 in range(0, len_ciphertext):
    #             for x18 in range(0, len_ciphertext):
    #                 for x19 in range(0, len_ciphertext):
    #                     for x20 in range(0, len_ciphertext):
    #                         for x21 in range(0, len_ciphertext):
    #                             error_values.add(1 << x16 | 1 << x16 | 1 << x18 | 1 << x19 | 1 << x20 | 1 << x21)
    #     print("6 bit error done")
    # if x == 7:
    #     for x22 in range(0, len_ciphertext):
    #         for x23 in range(0, len_ciphertext):
    #             for x24 in range(0, len_ciphertext):
    #                 for x25 in range(0, len_ciphertext):
    #                     for x26 in range(0, len_ciphertext):
    #                         for x27 in range(0, len_ciphertext):
    #                             for x28 in range(0, len_ciphertext):
    #                                 error_values.add(1 << x22 | 1 << x23 | 1 << x24 | 1 << x25 | 1 << x26 | 1 << x27 | 1 << x28)
    #     print("7 bit error done")
    # if x == 8:
    #     for x29 in range(0, len_ciphertext):
    #         for x30 in range(0, len_ciphertext):
    #             for x31 in range(0, len_ciphertext):
    #                 for x32 in range(0, len_ciphertext):
    #                     for x33 in range(0, len_ciphertext):
    #                         for x34 in range(0, len_ciphertext):
    #                             for x35 in range(0, len_ciphertext):
    #                                 for x36 in range(0, len_ciphertext): 
    #                                     error_values.add(1 << x29 | 1 << x30 | 1 << x31 | 1 << x32 | 1 << x33 | 1 << x34 | 1 << x35 | 1 << x36)
    #     print("8 bit error done")
sortedvalues = sorted(error_values)
for x in sortedvalues:
    dictionary.write(str(x)+"\n")