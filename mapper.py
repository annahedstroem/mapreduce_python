#!/usr/bin/python
import sys

def mapper():

    for line in sys.stdin:
        data = line.strip().split(',')

        # Retrieve the attributes of interest.
        city = data[-2]
        country = data[-1]

        # Print the {key, values} pairs that will be passed to the reducer.
        print("{0}\t{1}\t{2}".format(country, city, 1))

if __name__ == "__main__":
    mapper()
