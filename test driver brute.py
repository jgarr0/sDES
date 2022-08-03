# driver program for tests

from multiprocessing import freeze_support
from pydoc import plain
import errortesting as ert

# values to test
plaintexts = ["z", "hi"]#, "cat", "bomb"]
keys = [384, 797]#, 424, 987]
# keep IV constant as IV does not have to be secret
IV = 0x96

def main():
    f = open("bruteforce_test_result.txt", "w")
    for i in range(0, len(plaintexts)):
        results = []
        f.write("{} takes:\n".format(plaintexts[i]))
        results.append(ert.adderr(int(keys[i]), plaintexts[i], IV, j))
        f.write("\t{}\n".format(results[j-1]))
        f.flush()
    f.close()

if __name__ == '__main__':
    main()