#!/usr/bin/env python
"""Transcribe given DNA strand."""
import os
import sys


def main(path):
    """Transcribe given DNA strand."""
    # Open given file and read contents.
    file = open(path)
    content = file.read().strip()
    
    # Print DNA transcription.
    print(content.replace('T', 'U'))


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit('Provide a DNA strand file.')
    else:
        main(path=path)
