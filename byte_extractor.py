#!/usr/bin/python3

import argparse
import sys

STEP = 1024  # Step for manual seek (when file is not seekable)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count", "-c", type=int, default=-1,
        help="Number of characters to read")
    parser.add_argument("--offset", "-s", type=int, default=0, help="Offset")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("input", help="Input file; use - for standard input")
    args = parser.parse_args()

    if args.input == "-":
        f = sys.stdin
    else:
        f = open(args.input)

    # Read only the necessary bytes if it is possible
    if f.seekable():
        f.seek(args.offset)
        s = f.read(args.count)
    # Some files like sys.stdin are not seekable... Let's seek manually.
    else:

        n = 0
        while (n + STEP) < args.offset:
            # Read some bytes
            f.read(STEP)
            n += STEP

        # Read the remaining bytes to complete offset
        f.read(args.offset - n)

        # Read the wanted bytes
        s = f.read(args.count)

    if args.input != "-":
        f.close()

    if args.output:
        f = open(args.output, "w")
        f.write(s)
        f.close()
    else:
        print(s)
