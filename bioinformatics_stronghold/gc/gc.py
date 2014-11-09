#!/usr/bin/env python3
"""Identify the DNA string having the highest GC-content."""
import argparse
import io
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
    segments = content.split('>')

    LOG.debug('Content after split:\n{}\n'.format(segments))

    # Build a mapping of DNA ID to DNA strand.
    id_map = {}
    for segment in segments:
        if not segment:
            continue

        segment = io.StringIO(segment).read()
        lines = segment.split('\n')
        strand_id = lines[0]
        dna_strand = ''.join(lines[1:])
        id_map[strand_id] = dna_strand

    LOG.debug('ID map:\n{}\n'.format(id_map))

    # Calculate each strands GC-content.
    gc_map = {}
    for strand_id in id_map:
        gc_content = _calculate_gc_content(id_map[strand_id])
        gc_map[gc_content] = strand_id

    LOG.debug('GC map:\n{}\n'.format(gc_map))

    highest = max(gc_map)
    print('{}\n{}'.format(gc_map[highest], highest))


def _calculate_gc_content(strand):
    """Calculate the GC-content of the given DNA strand."""
    total_bases = len(strand)
    total_gc_bases = len(strand.replace('A', '').replace('T', ''))

    gc_percent = float(total_gc_bases) / float(total_bases) * 100
    return round(gc_percent, 6)


if __name__ == '__main__':
    configure_stream_logger()
    args = parse_args()
    main(args)
