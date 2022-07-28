#!/usr/bin/python3

'''
This file is part of Blokada.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright © 2022 Blocka AB. All rights reserved.

@author Karol Gusak (karol@blocka.net)
'''

'''
Generates a whitelist file out of whitelist sets (urls) and the manual whitelist.
'''

import sys
import os
import json
import getopt
from os import path
from datetime import datetime
from urllib.request import urlopen


def main(argv):

    def usage():
        print("usage: gen-whitelist.py [-o <whitelist>]")

    print("Gen-whitelist v0.1")

    base_path = "."
    config = {
        "input-manual": "./whitelist-manual",
        "input-sets": "./whitelist-sets",
        "output": "./whitelist",
    }

    try:
        opts, _ = getopt.getopt(argv, "o:")
    except getopt.GetoptError:
        print("  Bad parameters")
        usage()
        return 1

    for opt, arg in opts:
        if opt == "-o":
            config["output"] = arg
        else:
            print("  Unknown argument: %s" % opt)
            usage()
            return 2

    print(config)

    # load manual whitelist
    hosts = set()
    with open(path.join(base_path, config["input-manual"])) as f:
        whitelist = f.read().split("\n")
        hosts.update(whitelist)
        print(f"  Adding manual whitelist of {len(whitelist)} entries...")

    # load whitelists from the sets
    print("  Processing whitelist sets...")
    sets = []
    with open(path.join(base_path, config["input-sets"])) as f:
        sets = f.read().split("\n")
    counter = 0

    for link in sets:
        print(f"      {link}")

        f = urlopen(link)
        content = f.read().decode('utf-8')

        for line in content.splitlines():
            if line.startswith("#"):
                continue
            elif line.startswith("/"):
                continue
            elif line.startswith("!"):
                continue
            else:
                counter += 1
                line, separator, tail = line.partition("#")
                line = line.strip()
                line = line.strip("|^")
                if line:
                    hosts.add(line)

    # write converted format
    out_file = path.join(base_path, config["output"])
    print("  Writing to file '%s'..." % out_file)
    with open(out_file, "wt") as f_out:
        for entry in sorted(hosts):
            f_out.write(f"{entry}\n")

    print(f"Saved {len(hosts)} hosts (of {counter} lines)")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
