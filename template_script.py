#!/usr/bin/python
"""
Sample call:

  my_script.py --required_arg user_signup --properties user_id phone email
"""
import os
import sys, argparse


def main(argv):
    args = _parse_args(argv)
    # args are accessed like args.required_arg
    infile = _get_infile(args.file)
    _process_stream(infile)


def _parse_args(argv):
    # type: (Dict) -> argparse.Namespace
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', help='Path to the input file', required=False)
    # parser.add_argument('--required_arg', help='A required arg', required=True)
    # parser.add_argument('--properties', nargs='+',
    #                     help='At least one property is required', required=True)
    args = parser.parse_args(argv)
    # args are accessed like args.required_arg
    return args


def _get_infile(filepath):
    # type: (Text) -> BinaryIO
    """Return an opened file to read, or sys.stdin if filepath is None.
    Raises an OSError if filepath is non-None but doesn't exist."""
    if filepath is None:
        return sys.stdin
    else:
        if not os.path.exists(filepath):
            raise OSError('File does not exist: {}'.format(filepath))
        return open(filepath, 'r')


def _process_stream(instream):
    for line in instream.readlines():
        pass


if __name__ == '__main__':
    main(sys.argv[1:])
