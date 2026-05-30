#!/usr/bin/env python

import json
import sys
from collections import Counter

cfg ='''
{
    "dns": {
        "servers": [
        {
            "tag": "local-dns",
            "type": "https",
            "server": "1.1.1.1"
        }
        ]
    },
    "inbounds" : [
    {
        "type": "tun",
        "tag": "tun-in",
        "address": "172.19.0.1/30",
        "stack": "gvisor",
        "exclude_package": ["io.nekohasekai.sfa"]
    }
    ],
    "outbounds": [
        {
            "type": "direct",
            "tag": "direct"
        }
    ],
    "route": {
        "final": "autosel",
        "rules":[
            {
                "protocol": "dns",
                "outbound": "direct"
            }
        ]

    }

}
'''

def main():
    config1 = json.loads(sys.stdin.read())
    config = json.loads(cfg)
    config['outbounds'] += config1['outbounds']

    print(json.dumps(config, indent=2))

if __name__ == "__main__": main()

