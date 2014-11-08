#!/usr/bin/env python
"""Count the number of times each nucleobase appears in the strand."""
import os
import sys


def main(path):
    """Count the number of times each nucleobase appears in the strand."""
    # The file containing the DNA strand.
    file = open(path)
    content = file.read().strip()

    # Dict of nucleobase counts.
    chars = {
        'A': 0,
        'C': 0,
        'G': 0,
        'T': 0
    }

    # Iterate over strand.
    for char in content:
        chars[char] += 1

    # Print nucleobase count in order.
    print('{} {} {} {}'.format(chars['A'], chars['C'], chars['G'], chars['T']))


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit('Provide the file containing the DNA strand.')
    else:
        main(path=path)
