import argparse
import sys

from data_prep import mlf


class LastData:
    def __init__(self):
        self.punct = ""
        self.last_phone = ""
        self.durations = []

    def add_to(self, durations, duration_for_puct=True):
        if len(self.durations) > 0:
            for d in self.durations[:-1]:
                durations.append(d)

            if self.punct != "":
                if mlf.is_sil(self.last_phone):
                    if self.last_phone == "sil":
                        if duration_for_puct:
                            d = 10
                            if self.durations[-1] < d:
                                d = self.durations[-1] - 1
                            durations.append(d)
                            durations.append(self.durations[-1] - d)  # add remaining of sil
                        else:
                            durations.append(0)  # add zero for punctuation
                            durations.append(self.durations[-1])
                    else:
                        durations.append(self.durations[-1])
                else:
                    durations.append(0)  # add zero for punctuation
                    durations.append(self.durations[-1])
            else:
                durations.append(self.durations[-1])
        self.punct = ""
        self.durations = []
        self.last_phone = ""


def calc_duration(to, fr, shift, freq):
    to_ms = int(to) / 10000.0
    t_shift = 1000.0 * shift / freq
    return int(round((to_ms - fr * t_shift) / t_shift))


def fix_duration(v, v_max, shift):
    if v * shift <= v_max:
        return 1
    intervals = v_max / shift
    if (intervals + 1) < v:
        return int(intervals) + 1 - v
    return 0


def get_dur_str(durations):
    res = ""
    p = ""
    for d in durations:
        res = res + p + str(d)
        p = " "
    return res


def write_line(name, durations, file):
    print("%s %s 0" % (name, get_dur_str(durations)), file=file)


def update_durations(durations, df):
    if df > 0:
        durations[-1] += df
    else:
        i = len(durations) - 1
        while df < 0 <= i:
            v = durations[i]
            if v + df < 0:
                durations[i] = 0
                df += v
            else:
                durations[i] += df
                df = 0
            i -= 1
    return durations


def main(argv):
    parser = argparse.ArgumentParser(description="Convert mlf to durations for fastspeech2 training",
                                     epilog="E.g. cat input.mlf | " + sys.argv[0] + " > result.mlf",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--freq", default=22050, type=int, help="Point in one sec. Used to calculate shift duration",
                        required=True)
    parser.add_argument("--shift", default=256, type=int, help="Shift in points. Used to calculate shift duration",
                        required=True)
    parser.add_argument("--samplesFile", default='', type=str, help="File containing file samples", required=True)
    parser.add_argument('--dur-for-punct', action=argparse.BooleanOptionalAction)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    print("Reading samples file : %s" % args.samplesFile, file=sys.stderr)

    samples = {}
    with open(args.samplesFile) as f:
        lines = f.readlines()
        for line in lines:
            s_line = line.strip()
            if s_line:
                ls = s_line.split(' ')
                samples[ls[0]] = int(ls[1])
    print("Read samples file with %d lines" % len(samples), file=sys.stderr)

    lc, wc = 0, 0
    name, lf = "", 0
    durations = []
    ld = LastData()
    for line in sys.stdin:
        lc += 1
        s_line = line.strip()
        if s_line == "#!MLF!#":
            continue
        elif s_line.startswith("\""):
            if name != "":
                ld.add_to(durations, args.dur_for_punct)
                df = fix_duration(lf, samples[name], args.shift)
                durations = update_durations(durations, df)
                write_line(name, durations, sys.stdout)
                if df < 0:
                    print("Fix last interval {}, minus {}".format(name, df), file=sys.stderr)
            name = s_line.strip('""').replace(".lab", "")
            durations, lf = [], 0
        elif s_line == ".":
            continue
        else:
            m_line = mlf.from_str(line.rstrip())
            if m_line.is_word():
                ld.add_to(durations, args.dur_for_punct)
                ld.punct = m_line.punct
            dl = calc_duration(m_line.to, lf, args.shift, args.freq)
            lf += dl
            ld.durations.append(dl)
            ld.last_phone = m_line.ph

    ld.add_to(durations, args.dur_for_punct)
    df = fix_duration(lf, samples[name], args.shift)
    durations = update_durations(durations, df)
    write_line(name, durations, sys.stdout)
    if df < 0:
        print("Fix last interval {}, minus {}".format(name, df), file=sys.stderr)

    print("Read %d lines, %d words" % (lc, wc), file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
