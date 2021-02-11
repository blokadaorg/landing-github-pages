#!/usr/bin/python3

'''
This file is part of Blokada.

Blokada is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Blokada is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Blokada.  If not, see <https://www.gnu.org/licenses/>.

Copyright © 2020 Blocka AB. All rights reserved.

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
                "id": "energized",
                "configs": [
                    {
                        "name": "spark",
                        "urls": [
                            "https://block.energized.pro/spark/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "blu",
                        "urls": [
                            "https://block.energized.pro/blu/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "basic",
                        "urls": [
                            "https://block.energized.pro/basic/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "adult",
                        "urls": [
                            "https://block.energized.pro/porn/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "regional",
                        "urls": [
                            "https://block.energized.pro/extensions/regional/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "social",
                        "urls": [
                            "https://block.energized.pro/extensions/social/formats/domains.txt"
                        ]
                    },
                    {
                        "name": "ultimate",
                        "urls": [
                            "https://block.energized.pro/ultimate/formats/domains.txt"
                        ]
                    }
                ]
            },
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
                            "https://dbl.oisd.nl/light/"
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
                        "name": "porn",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/porn.txt"
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
            }
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
