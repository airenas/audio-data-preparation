import argparse
import sys

import range


def main(argv):
    parser = argparse.ArgumentParser(description="Makes bash commands for sox from range file",
                                     epilog="E.g. cat input.mlf | " + sys.argv[0] + " > result.sh",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--inDir", default='', type=str, help="Directory of wav input", required=True)
    parser.add_argument("--outDir", default='', type=str, help="Directory for wav output", required=True)
    parser.add_argument("--name", default='', type=str, help="Name of the wav file", required=True)
    args = parser.parse_args(args=argv)

    ranges = range.load_ranges(sys.stdin)

    for i, r in enumerate(ranges):
        print("sox %s/%s.wav %s/lab_%s_%03d.wav trim %f =%f" %
              (args.inDir, args.name, args.outDir, args.name, i, r.from_ / 10000000, r.to / 10000000),
              file=sys.stdout)

    print("Read %d lines" % len(ranges), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
