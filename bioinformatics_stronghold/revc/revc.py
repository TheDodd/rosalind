#!/usr/bin/env python3
"""Provide the reverse complement string."""
import argparse
import array
import logging
import os

# Root logger.
LOG = logging.getLogger()


class EnableVerbosity(argparse.Action):
    """Action class to enable verbosity when requested."""

    def __call__(self, parser, namespace, value, option_string):
        # Get the root logger.
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.debug('Verbosity enabled.')


def configure_stream_logger(logger):
    """Configure stream handler logging."""
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)


def define_parser():
    """Define the command-line parser."""
    parser = argparse.ArgumentParser()

    # A positional argument for the expected data set.
    parser.add_argument(
        'file',
        type=valid_file,
        help='The data set this program is to operate upon.'
    )

    # A flag to increase verbosity.
    parser.add_argument(
        '-v', '--verbose',
        action=EnableVerbosity,
        nargs=0,
        help='Enable verbose mode.'
    )

    return parser


def parse_args():
    """Parse command-line arguments."""
    parser = define_parser()
    args = parser.parse_args()
    LOG.debug('Arguments parsed:\n{}'.format(args))
    return args


def valid_file(path):
    """Ensure that the given file is valid."""
    if not os.path.isfile(path):
        LOG.debug("'{}' does not appear to be a valid file.".format(path))
        msg = 'The specified file must exist. Try using an absolute path.'
        raise argparse.ArgumentTypeError(msg)
    else:
        abspath = os.path.abspath(path)
        LOG.debug("'{}' is being used as data set.".format(abspath))
        return abspath


def main(args):
    """Main routine."""
    # Get the contents of the given file.
    file = open(args.file)
    content = file.read().strip()
    LOG.debug('Data set:\n{}'.format(content))

    # A mapping of base complements.
    base_complement_map = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }

    # An array of the complements of the given nucleotide string.
    complements = array.array('u')
    for char in content:
        complement = base_complement_map[char]
        complements.append(complement)
    LOG.debug('Parsed complements:\n{}'.format(complements))

    # Print the array of complements, reversed.
    complements.reverse()
    print(complements.tounicode())


if __name__ == '__main__':
    configure_stream_logger(LOG)
    args = parse_args()
    main(args)
