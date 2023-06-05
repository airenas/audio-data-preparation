import argparse
import sys
from typing import List

from data_prep import mlf
from data_prep.mlf import mlf_millis
from data_prep.range import Range


def is_split(m):
    return (m.ph == "sil" or m.ph == "sp") and m.sent == "sil"


def write_ranges(ranges, file):
    for r in ranges:
        print("%d %d" % (r.from_, r.to), file=file)


def try_join(data: List[Range], duration):
    res, c = [], None
    for r in data:
        if c is None:
            c = Range(r.from_, r.to)
        else:
            if r.to - c.from_ > duration:
                res.append(c)
                c = Range(r.from_, r.to)
            else:
                c.to = r.to
    if c is not None:
        res.append(c)
    return res


def main(argv):
    parser = argparse.ArgumentParser(description="Makes range file for mlf. Splits by sil",
                                     epilog="E.g. cat input.mlf | " + sys.argv[0] + " > result.range",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--maxSil", default=200, type=int, help="Max sil in ms", required=True)
    parser.add_argument("--splitInto", default=0, type=int, help="Interval size od secs to try splitting")
    args = parser.parse_args(args=argv)

    # print("Starting", file=sys.stderr)
    # print("Using max sil %d ms" % args.maxSil, file=sys.stderr)
    max_sil = args.maxSil * mlf_millis
    mlfs = []
    lc = 0
    for line in sys.stdin:
        lc += 1
        s_line = line.strip()
        if s_line == "#!MLF!#":
            continue
        elif s_line == ".":
            continue
        else:
            m_line = mlf.from_str(line.rstrip())
            mlfs.append(m_line)

    res = []
    r = None
    for i, m_line in enumerate(mlfs):
        from_ = int(m_line.from_)
        to = int(m_line.to)
        is_sp = is_split(m_line)
        if i == 0:
            r = Range(from_, to)
            if is_sp:
                r.from_ = trim_4(max(from_, to - max_sil))
            res.append(r)
        elif i == len(mlfs) - 1:
            r.to = to
            if is_sp:
                r.to = trim_4(min(to, from_ + max_sil))
        elif is_sp:
            at = from_ + (to - from_) / 2
            at = trim_4(at)
            r.to = trim_4(min(at, from_ + max_sil))
            r = Range(trim_4(max(at, to - max_sil)), to)
            res.append(r)

    if args.splitInto > 0:
        # try to join intervals to be not longer by `args.splitInto` secs
        res = try_join(res, args.splitInto * 1000 * mlf_millis)
    write_ranges(res, sys.stdout)

    print("Read %d lines, %d splits" % (lc, len(res)), file=sys.stderr)
    # print("Done", file=sys.stderr)


def trim_4(n):
    return int(n / 10000) * 10000


if __name__ == "__main__":
    main(sys.argv[1:])
