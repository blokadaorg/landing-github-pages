#!/usr/bin/python3

'''
This file is part of Blokada.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright © 2021 Blocka AB. All rights reserved.

@author Karol Gusak (karol@blocka.net)
'''

'''
Extracts Exodus Privacy data into a simple (naive) hostlist.
'''

import sys
import os
import json
import getopt
import urllib.request
from os import path
from datetime import datetime

def main(argv):

    def usage():
        print("usage: exodus.py -i trackers-url [-o <hostlist>]")

    print("Exodus extractor v0.1")

    base_path = "."
    config = {
        "input": "https://reports.exodus-privacy.eu.org/api/trackers",
        "output": "../blocklists/exodusprivacy/standard/hosts.txt",
        "whitelistedSubdomains": ["www", "api", "cdn"]
    }

    try:
        opts, _ = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError:
        print("  Bad parameters")
        usage()
        return 1

    for opt, arg in opts:
        if opt == "-i":
            config["input"] = arg
        elif opt == "-o":
            config["output"] = arg
        else:
            print("  Unknown argument: %s" % opt)
            usage()
            return 2

    # check for mandatory parameters
    if not config["input"]:
        print("  Missing input parameter")
        usage()
        return 3

    print(config)

    # load whitelist if any
    with open(path.join(base_path, "whitelist")) as f:
        whitelist = f.read().split("\n")

    print(whitelist)

    # load all domain files
    print("  Processing Exodus trackers...")
    domains = []
    page = urllib.request.urlopen(config["input"])
    trackers = json.loads(page.read())["trackers"]
    counter = 0

    for key in trackers.keys():
        for host in cleanup(trackers[key]["network_signature"]).split("|"):
            if not host:
                continue

            if host.startswith("."):
                host = host[1:]

            if host in whitelist:
                print(f"  Skipping (whitelisted): {host}")
                continue

            if host.split(".")[0] in config["whitelistedSubdomains"]:
                print(f"  Skipping (whitelisted subdomain): {host}")
                continue

            if host.split(".")[0] == "*":
                print(f"  Skipping (wildcard): {host}")
                continue

            domains.append(host)
            counter += 1

    # write converted format
    out_file = path.join(base_path, config["output"])
    print("  Writing to file '%s'..." % out_file)
    with open(out_file, "wt") as f_out:
        f_out.write("# exodusprivacy standard\n")
        f_out.write("# This host file is based on Exodus Privacy database.\n")
        f_out.write("# More info at https://go.blokada.org/exodusprivacy\n")
        f_out.write(f"# Generated at {datetime.now()}\n")
        f_out.write("# Made by Blokada\n\n")

        for entry in domains:
            f_out.write(f"{entry}\n")

    print(f"Extracted {counter} hosts")

def cleanup(host) -> str:
    if host in (".", "NC"):
        return None
    else:
        return host.replace("\\", "", -1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
