#! /usr/bin/env python3
import sys
import re
from hashlib import sha256

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], '<process PID>', file=sys.stderr)
        exit(1)

    pid = sys.argv[1]

    # maps contains the mapping of memory of a specific project
    map_file = f"/proc/{pid}/maps"
    mem_file = f"/proc/{pid}/mem"

    # iterate over regions
    with open(map_file, 'r') as map_f, open(mem_file, 'rb', 0) as mem_f:
        for line in map_f.readlines():  # for each mapped region
            m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) (.{4})', line)
            if "r" in m.group(3) and "x" in m.group(3):  # readable region
                start = int(m.group(1), 16)
                end = int(m.group(2), 16)
                mem_f.seek(start)  # seek to region start
                try:
                    chunk = mem_f.read(end - start)  # read region contents
                    print(sha256(chunk).hexdigest())  # dump contents to standard output
                    break
                except OSError:
                    print(hex(start), '-', hex(end), '[error,skipped]', file=sys.stderr)
                    break