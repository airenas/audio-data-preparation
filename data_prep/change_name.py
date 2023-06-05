import argparse
import sys


def is_name(line):
    return line.startswith("\"")


def update(line, prefix):
    return "\"" + prefix + line.lstrip("\"")


def main(argv):
    parser = argparse.ArgumentParser(description="Change segment name - add speaker",
                                     epilog="E.g. cat input.mlf | " + sys.argv[0] + " > result.mlf",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--prefix", default='SAB_', type=str, help="Add prefix", required=False)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc = 0
    for line in sys.stdin:
        lc += 1
        line = line.rstrip()
        if is_name(line) and args.prefix:
            line = update(line, args.prefix)
        print(line)
    print("Read %d lines" % lc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
