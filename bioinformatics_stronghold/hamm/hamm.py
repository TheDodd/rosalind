#!/usr/bin/env python3
"""Template for processing DNA & RNA data sets."""
import argparse
import logging
import os

LOG = logging.getLogger()


class EnableVerbosity(argparse.Action):
    """Action class to enable verbosity when requested."""

    def __call__(self, parser, namespace, value, option_string):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.debug('Verbosity enabled.')


def configure_stream_logger():
    """Configure stream handler for root logger."""
    logger = logging.getLogger()
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

    # An option to increase verbosity.
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
    file = open(args.file)
    content = file.read().strip()

    LOG.debug('Content:\n{}'.format(content))

    # Get both strings to calculate Hamming distance.
    string1, string2 = content.split('\n')

    LOG.debug('Lines:\n{}\n{}'.format(string1, string2))

    distance = 0
    for char1, char2 in zip(string1, string2):
        if char1 != char2:
            distance += 1

    print(distance)


if __name__ == '__main__':
    configure_stream_logger()
    args = parse_args()
    main(args)
