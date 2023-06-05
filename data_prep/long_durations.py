import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description="Detect long durations",
                                     epilog="E.g. cat durations | " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--duration", default=150, type=int, help="Duration len in points to indicate a problem",
                        required=False)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    i, p = 0, 0
    for d in sys.stdin.readlines():
        i += 1
        words = d.split()
        la = [k for k in words[1:]]
        il = [int(k) for k in la]
        gt = [k for k in il if k > args.duration]
        if len(gt) > 0:
            p += 1
            print(words[0], gt)

    print("Read %d lines. Possible problems %d" % (i, p), file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
