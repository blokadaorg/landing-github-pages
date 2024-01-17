#!/usr/bin/python3

"""
This file is part of Blokada.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright © 2021 Blocka AB. All rights reserved.

@author Karol Gusak (karol@blocka.net)
"""

"""
Downloads blocklists used by Blokada to make a mirror.

Packs are configured with a simple structure:
- id: id of the pack, important for the clients
- configs: list of configurations (lists for this pack)
- addwildcards (optional): if true, will prefix all lines for all
  lists of this pack with a wildcard

Each configuration has:
- name: name of the list, important for the clients
- urls: list of urls to download the list from (first successful)
- merge: a filename to merge with the downloaded list (optional)

"""

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
                "id": "oisd",
                "configs": [
                    {
                        "name": "small",
                        "urls": ["https://small.oisd.nl/"],
                    },
                    {
                        "name": "big",
                        "urls": ["https://big.oisd.nl/"],
                    },
                    {
                        "name": "nsfw",
                        "urls": ["https://nsfw.oisd.nl/"],
                    },
                ],
            },
            {
                "id": "stevenblack",
                "configs": [
                    {
                        "name": "unified",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
                        ],
                    },
                    {
                        "name": "fakenews",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts"
                        ],
                    },
                    {
                        "name": "fake news",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts"
                        ],
                    },
                    {
                        "name": "adult",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts"
                        ],
                    },
                    {
                        "name": "social",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social/hosts"
                        ],
                    },
                    {
                        "name": "gambling",
                        "urls": [
                            "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts"
                        ],
                    },
                ],
            },
            {
                "id": "goodbyeads",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt"
                        ],
                    },
                    {
                        "name": "youtube",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-YouTube-AdBlock.txt"
                        ],
                    },
                    {
                        "name": "samsung",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt"
                        ],
                    },
                    {
                        "name": "xiaomi",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt"
                        ],
                    },
                    {
                        "name": "spotify",
                        "urls": [
                            "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt"
                        ],
                    },
                ],
            },
            {
                "id": "adaway",
                "configs": [
                    {"name": "standard", "urls": ["https://adaway.org/hosts.txt"]}
                ],
            },
            {
                "id": "phishingarmy",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://phishing.army/download/phishing_army_blocklist.txt"
                        ],
                    },
                    {
                        "name": "extended",
                        "urls": [
                            "https://phishing.army/download/phishing_army_blocklist_extended.txt"
                        ],
                    },
                ],
            },
            {
                "id": "ddgtrackerradar",
                "configs": [
                    {
                        "name": "standard",
                        "urls": ["../blocklists/ddgtrackerradar/standard/hosts.txt"],
                    }  # ,
                    # {
                    #     "name": "extended",
                    #     "urls": [
                    #         "https://blokada.org/blocklists/ddgtrackerradar/extended/hosts.txt"
                    #     ]
                    # }
                ],
            },
            {
                "id": "blacklist",
                "configs": [
                    {
                        "name": "adservers",
                        "urls": [
                            "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"
                        ],
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt"
                        ],
                    },
                ],
            },
            {
                "id": "exodusprivacy",
                "configs": [
                    {
                        "name": "standard",
                        "urls": ["../blocklists/exodusprivacy/standard/hosts.txt"],
                    }
                ],
            },
            {
                "id": "developerdan",
                "configs": [
                    {
                        "name": "ads and tracking",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt"
                        ],
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/facebook-extended.txt"
                        ],
                    },
                    {
                        "name": "amp",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/amp-hosts-extended.txt"
                        ],
                    },
                    {
                        "name": "hate and junk",
                        "urls": [
                            "https://www.github.developerdan.com/hosts/lists/hate-and-junk-extended.txt"
                        ],
                    },
                ],
            },
            {
                "id": "blocklist",
                "configs": [
                    {
                        "name": "ads",
                        "urls": ["https://blocklistproject.github.io/Lists/ads.txt"],
                    },
                    {
                        "name": "facebook",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/facebook.txt"
                        ],
                    },
                    {
                        "name": "malware",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/malware.txt"
                        ],
                    },
                    {
                        "name": "phishing",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/phishing.txt"
                        ],
                    },
                    {
                        "name": "tracking",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/tracking.txt"
                        ],
                    },
                    {
                        "name": "youtube",
                        "urls": [
                            "https://blocklistproject.github.io/Lists/youtube.txt"
                        ],
                    },
                ],
            },
            {
                "id": "spam404",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt"
                        ],
                    }
                ],
            },
            {
                "id": "hblock",
                "configs": [
                    {
                        "name": "standard",
                        "urls": ["https://hblock.molinero.dev/hosts_domains.txt"],
                    }
                ],
            },
            {
                "id": "cpbl",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/bongochong/CombinedPrivacyBlockLists/master/newhosts-final.hosts"
                        ],
                    },
                    {
                        "name": "mini",
                        "urls": [
                            "https://raw.githubusercontent.com/bongochong/CombinedPrivacyBlockLists/master/MiniLists/mini-newhosts.hosts"
                        ],
                    },
                ],
            },
            {
                "id": "danpollock",
                "configs": [
                    {
                        "name": "standard",
                        "urls": ["https://someonewhocares.org/hosts/hosts"],
                    }
                ],
            },
            {
                "id": "urlhaus",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-hosts.txt"
                        ],
                    }
                ],
            },
            {
                "id": "1hosts",
                "configs": [
                    {
                        "name": "lite (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt"
                        ],
                    },
                    {
                        "name": "pro (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Pro/adblock.txt"
                        ],
                    },
                    {
                        "name": "xtra (wildcards)",
                        "urls": [
                            "https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt"
                        ],
                    },
                ],
            },
            {
                "id": "d3host",
                "configs": [
                    {
                        "name": "standard",
                        "urls": [
                            "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.txt"
                        ],
                    }
                ],
            },
            {
                "id": "ut1",
                "configs": [
                    {
                        "name": "dating",
                        "urls": [
                            "https://raw.githubusercontent.com/olbat/ut1-blacklists/master/blacklists/dating/domains"
                        ],
                    },
                    {
                        "name": "gambling",
                        "urls": [
                            "https://raw.githubusercontent.com/olbat/ut1-blacklists/master/blacklists/gambling/domains",
                        ],
                    },
                    {
                        "name": "gaming",
                        "urls": [
                            "https://raw.githubusercontent.com/olbat/ut1-blacklists/master/blacklists/games/domains"
                        ],
                    },
                    {
                        "name": "social",
                        "urls": [
                            "https://raw.githubusercontent.com/olbat/ut1-blacklists/master/blacklists/social_networks/domains"
                        ],
                    },
                    {
                        "name": "warez",
                        "urls": [
                            "https://raw.githubusercontent.com/olbat/ut1-blacklists/master/blacklists/warez/domains"
                        ],
                    },
                ],
            },
            {
                "id": "sinfonietta",
                "configs": [
                    {
                        "name": "gambling",
                        "urls": [
                            "https://raw.githubusercontent.com/Sinfonietta/hostfiles/master/gambling-hosts"
                        ],
                    },
                    {
                        "name": "porn",
                        "urls": [
                            "https://raw.githubusercontent.com/Sinfonietta/hostfiles/master/pornography-hosts"
                        ],
                    },
                    {
                        "name": "social",
                        "urls": [
                            "https://raw.githubusercontent.com/Sinfonietta/hostfiles/master/social-hosts"
                        ],
                    },
                ],
            },
            {
                "id": "tiuxo",
                "configs": [
                    {
                        "name": "porn",
                        "urls": [
                            "https://raw.githubusercontent.com/tiuxo/hosts/master/porn"
                        ],
                    },
                ],
            },
            {
                "id": "mhxion",
                "configs": [
                    {
                        "name": "porn",
                        "urls": [
                            "https://raw.githubusercontent.com/mhxion/pornaway/master/hosts/porn_sites.txt"
                        ],
                    },
                ],
            },
            {
                "id": "ndnspiracy",
                "addwildcard": True,
                "configs": [
                    {
                        "name": "dht bootstrap nodes",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/dht-bootstrap-nodes"
                        ],
                    },
                    {
                        "name": "file hosting",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/file-hosting"
                        ],
                    },
                    {
                        "name": "proxies",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/proxies"
                        ],
                    },
                    {
                        "name": "streaming audio",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/streaming-audio"
                        ],
                    },
                    {
                        "name": "streaming video",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/streaming-video"
                        ],
                    },
                    {
                        "name": "torrent clients",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/torrent-clients"
                        ],
                    },
                    {
                        "name": "torrent trackers",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/torrent-trackers"
                        ],
                    },
                    {
                        "name": "torrent websites",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/torrent-websites"
                        ],
                    },
                    {
                        "name": "usenet",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/usenet"
                        ],
                    },
                    {
                        "name": "warez",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/piracy-blocklists/master/warez"
                        ],
                    },
                ],
            },
            {
                "id": "ndnsapps",
                "addwildcard": True,
                "configs": [
                    {
                        "name": "9gag",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/9gag"
                        ],
                    },
                    {
                        "name": "amazon",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/amazon"
                        ],
                    },
                    {
                        "name": "bereal",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/bereal"
                        ],
                    },
                    {
                        "name": "blizzard",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/blizzard"
                        ],
                    },
                    {
                        "name": "chatgpt",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/chatgpt"
                        ],
                    },
                    {
                        "name": "dailymotion",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/dailymotion"
                        ],
                    },
                    {
                        "name": "discord",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/discord"
                        ],
                    },
                    {
                        "name": "disneyplus",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/disneyplus"
                        ],
                    },
                    {
                        "name": "ebay",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/ebay"
                        ],
                    },
                    {
                        "name": "facebook",
                        "merge": "./merge-facebook",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/facebook"
                        ],
                    },
                    {
                        "name": "fortnite",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/fortnite"
                        ],
                    },
                    {
                        "name": "google-chat",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/google-chat"
                        ],
                    },
                    {
                        "name": "hbomax",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/hbomax"
                        ],
                    },
                    {
                        "name": "hulu",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/hulu"
                        ],
                    },
                    {
                        "name": "imgur",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/imgur"
                        ],
                    },
                    {
                        "name": "instagram",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/instagram"
                        ],
                    },
                    {
                        "name": "leagueoflegends",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/leagueoflegends"
                        ],
                    },
                    {
                        "name": "mastodon",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/mastodon"
                        ],
                    },
                    {
                        "name": "messenger",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/messenger"
                        ],
                    },
                    {
                        "name": "minecraft",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/minecraft"
                        ],
                    },
                    {
                        "name": "netflix",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/netflix"
                        ],
                    },
                    {
                        "name": "pinterest",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/pinterest"
                        ],
                    },
                    {
                        "name": "playstation-network",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/playstation-network"
                        ],
                    },
                    {
                        "name": "primevideo",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/primevideo"
                        ],
                    },
                    {
                        "name": "reddit",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/reddit"
                        ],
                    },
                    {
                        "name": "roblox",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/roblox"
                        ],
                    },
                    {
                        "name": "signal",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/signal"
                        ],
                    },
                    {
                        "name": "skype",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/skype"
                        ],
                    },
                    {
                        "name": "snapchat",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/snapchat"
                        ],
                    },
                    {
                        "name": "spotify",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/spotify"
                        ],
                    },
                    {
                        "name": "steam",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/steam"
                        ],
                    },
                    {
                        "name": "telegram",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/telegram"
                        ],
                    },
                    {
                        "name": "tiktok",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/tiktok"
                        ],
                    },
                    {
                        "name": "tinder",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/tinder"
                        ],
                    },
                    {
                        "name": "tumblr",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/tumblr"
                        ],
                    },
                    {
                        "name": "twitch",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/twitch"
                        ],
                    },
                    {
                        "name": "twitter",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/twitter"
                        ],
                    },
                    {
                        "name": "vimeo",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/vimeo"
                        ],
                    },
                    {
                        "name": "vk",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/vk"
                        ],
                    },
                    {
                        "name": "whatsapp",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/whatsapp"
                        ],
                    },
                    {
                        "name": "xboxlive",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/xboxlive"
                        ],
                    },
                    {
                        "name": "youtube",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/youtube"
                        ],
                    },
                    {
                        "name": "zoom",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/services/main/services/zoom"
                        ],
                    },
                ],
            },
            {
                "id": "safesearch",
                "configs": [
                    {
                        "name": "nosafesearch",
                        "urls": [
                            "https://raw.githubusercontent.com/nextdns/no-safesearch/main/domains"
                        ],
                    },
                ],
            },
        ],
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
            directory = os.path.join(
                base_path, config["output"], pack["id"], cfg["name"]
            )
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, "hosts.txt")
            try:
                print(f"  Downloading: {url}")

                if url.startswith("http"):
                    opener = urllib.request.build_opener()
                    opener.addheaders = [
                        (
                            "User-agent",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                        )
                    ]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, file_path)
                else:
                    copyfile(url, file_path)

                # Merge additional hosts when specified
                merge = cfg.get("merge")
                if merge:
                    print(f"  Merging custom hosts: {merge}")
                    with open (os.path.join(base_path, merge), "r") as file:
                        lines = file.readlines()
                    with open(file_path, "a") as file:
                        for line in lines:
                            file.write(line)

                # Check if 'addwildcard' is set in config and then prefix lines
                if pack.get("addwildcard"):
                    print(f"  Adding wildcards: {file_path}")
                    with open(file_path, "r") as file:
                        lines = file.readlines()
                    with open(file_path, "w") as file:
                        for line in lines:
                            file.write(f"*.{line}")

                count += 1
            except Exception as e:
                print(f"Failed downloading: {url}")
                print(e)
                failedCount += 1

    print(f"Done. Downloaded {count} out of {count + failedCount}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
