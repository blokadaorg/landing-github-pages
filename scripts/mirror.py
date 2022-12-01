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
Downloads blocklists used by Blokada to make a mirror.
'''

import sys
import os
import getopt
import urllib.request
from shutil import copyfile

def main(argv):

    # def usage():
    #     print("usage: mirror.py")
    #     print("Outputs all lists to ./mirror")

    print("Blokada blocklists mirror v0.1")

    base_path = "."
    config = {
        "mode": "v5",
        "output": "../mirror/v5",
        "packs": [
            {
                "id": "stevenblack",
                "configs": [
                    {
                        "name": "unified",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
                        ]
                    },
                    {
                        "name": "fakenews",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts"
                        ]
                    },
                    {
                        "name": "fake news",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts"
                        ]
                    },
                    {
                        "name": "adult",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts"
                        ]
                    },
                    {
                        "name": "social",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social/hosts"
                        ]
                    },
                    {
                        "name": "gambling",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts"
                        ]
                    },
                ]
            },
            {
                "id": "goodbyeads",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt"
                        ]
                    },
                    {
                        "name": "youtube",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-YouTube-AdBlock.txt"
                        ]
                    },
                    {
                        "name": "samsung",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt"
                        ]
                    },
                    {
                        "name": "xiaomi",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt"
                        ]
                    },
                    {
                        "name": "spotify",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt"
                        ]
                    }

                ]
            },
            {
                "id": "adaway",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://adaway.org/hosts.txt"
                        ]
                    }
                ]
            },
            {
                "id": "phishingarmy",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://phishing.army/download/phishing_army_blocklist.txt"
                        ]
                    },
                    {
                        "name": "extended",
                        "urls": [
                            "https://phishing.army/download/phishing_army_blocklist_extended.txt"
                        ]
                    }
                ]
            },
            {
                "id": "ddgtrackerradar",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "../blocklists/ddgtrackerradar/standard/hosts.txt"
                        ]
                    }#,
                    # {
                    #     "name": "extended",
                    #     "urls": [
                    #         "https://blokada.org/blocklists/ddgtrackerradar/extended/hosts.txt"
                    #     ]
                    # }
                ]
            },
            {
                "id": "blacklist",
                "configs": [
                    {
                        "name": "adservers",
                        "urls": [
                            "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"
                        ]
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt"
                        ]
                    }
                ]
            },
            {
                "id": "exodusprivacy",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "../blocklists/exodusprivacy/standard/hosts.txt"
                        ]
                    }
                ]
            },
            {
                "id": "oisd",
                "configs": [
                    {
                        "name": "light",
                        "urls": [
                            "https://dbl.oisd.nl/basic/"
                        ]
                    },
                    {
                        "name": "basicw",
                        "urls": [
                            "https://dblw.oisd.nl/basic/"
                        ]
                    },
                    {
                        "name": "basica",
                        "urls": [
                            "https://abp.oisd.nl/basic/"
                        ]
                    },
                    {
                        "name": "basic (wildcards)",
                        "urls": [
                            "https://abp.oisd.nl/basic/"
                        ]
                    },
                    {
                        "name": "extra (wildcards)",
                        "urls": [
                            "https://abp.oisd.nl/extra/"
                        ]
                    }
                ]
            },
            {
                "id": "developerdan",
                "configs": [
                    {
                        "name": "ads",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt"
                        ]
                    },
                    {
                        "name": "ads and tracking",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt"
                        ]
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/facebook-extended.txt"
                        ]
                    },
                    {
                        "name": "amp",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/amp-hosts-extended.txt"
                        ]
                    },
                    {
                        "name": "junk",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/hate-and-junk-extended.txt"
                        ]
                    },
                    {
                        "name": "hate and junk",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/hate-and-junk-extended.txt"
                        ]
                    }
                ]
            },
            {
                "id": "blocklist",
                "configs": [
                    {
                        "name": "ads",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/ads.txt"
                        ]
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/facebook.txt"
                        ]
                    },
                    {
                        "name": "malware",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/malware.txt"
                        ]
                    },
                    {
                        "name": "phishing",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/phishing.txt"
                        ]
                    },
                    {
                        "name": "tracking",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/tracking.txt"
                        ]
                    },
                    {
                        "name": "youtube",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/youtube.txt"
                        ]
                    }
                ]
            },
            {
                "id": "spam404",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt"
                        ]
                    }
                ]
            },
            {
                "id": "hblock",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://hblock.molinero.dev/hosts_domains.txt"
                        ]
                    }
                ]
            },
            {
                "id": "cpbl",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/bongochong/CombinedPrivacyBlockLists/master/newhosts-final.hosts"
                        ]
                    },
                    {
                        "name": "mini",
                        "urls": [
                            "https://raw.githubusercontent.com/bongochong/CombinedPrivacyBlockLists/master/MiniLists/mini-newhosts.hosts"
                        ]
                    }
                ]
            },
            {
                "id": "danpollock",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://someonewhocares.org/hosts/hosts"
                        ]
                    }
                ]
            },
            {
                "id": "urlhaus",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-hosts.txt"
                        ]
                    }
                ]
            },
            {
                "id": "1hosts",
                "configs": [
                    {
                        "name": "lite",
                        "urls": [
                            "https://badmojr.github.io/1Hosts/Lite/hosts.txt"
                        ]
                    },
                    {
                        "name": "pro",
                        "urls": [
                            "https://badmojr.github.io/1Hosts/Pro/hosts.txt"
                        ]
                    },
                    {
                        "name": "litea",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt"
                        ]
                    },
                    {
                        "name": "proa",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Pro/adblock.txt"
                        ]
                    },
                    {
                        "name": "xtraa",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt"
                        ]
                    },
                    {
                        "name": "lite (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt"
                        ]
                    },
                    {
                        "name": "pro (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Pro/adblock.txt"
                        ]
                    },
                    {
                        "name": "xtra (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt"
                        ]
                    }
                ]
            },
            {
                "id": "d3host",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.txt"
                        ]
                    }
                ]
            },
        ]
    }

    # try:
    #     opts, _ = getopt.getopt(argv, "i:o:")
    # except getopt.GetoptError:
    #     print("  Bad parameters")
    #     usage()
    #     return 1

    # for opt, arg in opts:
    #     if opt == "-i":
    #         config["input"] = arg
    #     elif opt == "-o":
    #         config["output"] = arg
    #     else:
    #         print("  Unknown argument: %s" % opt)
    #         usage()
    #         return 2

    # # check for mandatory parameters
    # if not config["input"]:
    #     print("  Missing input parameter")
    #     usage()
    #     return 3

    print("")
    print(config)
    print("")

    count = 0
    failedCount = 0
    for pack in config["packs"]:
        for cfg in pack["configs"]:
            url = cfg["urls"][0]
            directory = os.path.join(base_path, config["output"], pack["id"], cfg["name"])
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                print(f"  Downloading: {url}")

                if url.startswith("http"):
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, os.path.join(directory, "hosts.txt"))
                else:
                    copyfile(url, os.path.join(directory, "hosts.txt"))

                count += 1
            except Exception as e:
                print(f"Failed downloading: {url}")
                print(e)
                failedCount += 1

    print(f"Done. Downloaded {count} out of {count + failedCount}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
