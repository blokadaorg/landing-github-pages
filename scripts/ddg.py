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
Extracts DuckDuckGo Tracker Radar data into a simple (naive) hostlist.
'''

import sys
import os
import json
import getopt
from os import path
from datetime import datetime

def main(argv):

    def usage():
        print("usage: ddg.py -i <ddg-repo> [-o <hostlist>]")

    print("DDG extractor v0.1")

    base_path = "."
    config = {
        "input": "../tracker-radar",
        "output": "../blocklists/ddgtrackerradar/standard/hosts.txt",
        "minResources": 3,
        "minResourcesPerSubdomain": 3,
        "whitelistedCategories": ["CDN", "Online Payment", "Non-Tracking"],
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

    print("Whitelist:")
    print(whitelist)

    # load whitelisted subdomains if any
    whitelistedSubdomains = []
    with open(path.join(base_path, "whitelist-subdomains")) as f:
        wsInput = f.read().split("\n")
        for ws in wsInput:
            if ws:
                whitelistedSubdomains.append(ws)
                for x in range(10):
                    whitelistedSubdomains.append(ws + str(x))

    print("Whitelisted subdomains:")
    print(whitelistedSubdomains)

    # load all domain files
    print("  Processing DuckDuckGo repo...")
    domains = []
    repo_dir = path.join(base_path, config["input"], "domains")
    counter = 0

    for region in os.listdir(repo_dir):
        region_dir = os.path.join(repo_dir, region)
        for filename in os.listdir(region_dir):
            with open(os.path.join(region_dir, filename), 'r') as f:
                domain = json.loads(f.read())
                if domain["domain"] in whitelist:
                    print(f"  Skipping (whitelisted): {domain['domain']}")
                    continue

                if len(domain["categories"]) > 0 and len(intersection(config["whitelistedCategories"], domain["categories"])) > 0:
                    print(f"  Skipping (whitelisted category): {domain['domain']} - {domain['categories']}")
                    continue

                if len(domain["resources"]) < config["minResources"]:
                    #print(f"  Skipping (not enough resources): {domain['domain']}")
                    continue

                if len(domain["subdomains"]) < 0:
                    #print(f"  Skipping (no subdomains): {domain['domain']}")
                    domains.append(domain["domain"])
                    counter += 1
                else:
                    for subdomain in domain["subdomains"]:
                        if subdomain in whitelistedSubdomains:
                            print(f"  Skipping (whitelisted subdomain): {subdomain}.{domain['domain']}")
                            continue

                        matchesWhitelistedSubdomain = False
                        for sub in whitelistedSubdomains:
                            if subdomain.startswith(sub):
                                matchesWhitelistedSubdomain = True
                                break

                        if matchesWhitelistedSubdomain:
                            print(f"  Skipping (whitelisted subdomain prefix): {subdomain}.{domain['domain']}")
                            continue

                        resourcesPerSubdomain = 0
                        for resource in domain["resources"]:
                            if subdomain in resource["subdomains"]:
                                resourcesPerSubdomain += 1

                        if resourcesPerSubdomain < config["minResourcesPerSubdomain"]:
                            #print(f"  Skipping (not enough resources per subdomain): {subdomain}.{domain['domain']}")
                            continue

                        full_domain = f"{subdomain}.{domain['domain']}"

                        if full_domain in whitelist:
                            print(f"  Skipping (whitelisted): {full_domain}")
                            continue

                        domains.append(full_domain)
                        counter += 1

    # write converted format
    out_file = path.join(base_path, config["output"])
    print("  Writing to file '%s'..." % out_file)
    with open(out_file, "wt") as f_out:
        f_out.write("# ddgtrackerradar standard\n")
        f_out.write("# This host file is based on DuckDuckGo Tracker Radar.\n")
        f_out.write("# More info at https://go.blokada.org/ddgtrackerradar\n")
        f_out.write(f"# Generated at {datetime.now()}\n")
        f_out.write("# Made by Blokada\n\n")

        domains = sorted(set(domains))
        for entry in domains:
            f_out.write(f"{entry}\n")

    print(f"Extracted {counter} hosts")

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
