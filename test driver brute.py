# driver program for tests

from multiprocessing import freeze_support
from pydoc import plain
import errortesting as ert

# values to test
plaintexts = ["z", "g", "i", "hi", "dr", "ko", "cat", "sav", "joe"] #, "bomb", "blue", "tran"]
keys = [384, 386, 971, 797, 639, 457, 424, 673, 495] #, 987, 795, 931]
# keep IV constant as IV does not have to be secret
IV = 0x96

def main():
    f = open("bruteforce_test_result.txt", "w")
    for i in range(0, len(plaintexts)):
        results = []
        f.write("{} takes:\n".format(plaintexts[i]))
        for j in range (1, 9):
            results.append(ert.adderr(int(keys[i]), plaintexts[i], IV, j))
            f.write("\t{}\n".format(results[j-1]))
            f.flush()
    f.close()

if __name__ == '__main__':
    main()