# driver program for tests

from pydoc import plain
import noerrortesting as nrt

# values to test
plaintexts = ["z", "hi", "cat", "bomb"]
keys = [384, 797, 424, 987]
# keep IV constant as IV does not have to be secret
IV = 0x96

def main():
    f = open("no_error_test_result.txt", "w")
    for i in range(0, len(plaintexts)):
        results = []
        f.write("{} takes:\n".format(plaintexts[i]))
        results.append(nrt.test(int(keys[i]), plaintexts[i], IV))
        f.write("\t{}\n".format(results[0]))
        f.flush()
    f.close()

if __name__ == '__main__':
    main()