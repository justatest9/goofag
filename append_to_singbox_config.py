#!/usr/bin/env python

import json
import sys
from collections import Counter
import base64
import yarl

cfg ='''
{
    "experimental": {
        "clash_api": {
            "external_controller": "127.0.0.1:9090"
        }
    },
    "dns": {
        "strategy": "ipv4_only",
        "servers": [
        {
            "tag": "doh",
            "type": "https",
            "server": "1.1.1.1",
            "server_port": 443,
            "path": "/dns-query",
            "tls": {
                "enabled": true,
                "server_name": "cloudflare-dns.com"
            }
        }
        ],
        "final": "doh"
    },
    "inbounds" : [
    {
        "type": "tun",
        "tag": "tun-in",
        "mtu": 1280,
        "address": "172.19.0.1/30",
        "stack": "gvisor",
        "auto_route": true,
        "strict_route": true,
        "exclude_package": ["io.nekohasekai.sf1a"]
    }
    ],
    "outbounds": [
        {
            "type": "direct",
            "tag": "direct"
        },
        {
            "type": "socks",
            "tag": "hideme",
            "server": "",
            "server_port": ""
        }
    ],
    "route": {
        "final": "autosel",
        "auto_detect_interface": true,
        "rules":[
            {
                "action": "sniff"
            },
            {
                "port": 53,
                "action": "hijack-dns"
            },
            {
                "package_name" : [
                    "ru.oneme.app",
                    "ru.ozon.app.android"
                ],
                "outbound": "direct"
            },
            {
                "domain_suffix": ["ru", "su", "yandex.com", "yandex.net", ".xn--p1ai"],
                "outbound": "direct"
            },
            {
                "domain_suffix" : [
                    "youtube.com",
                    "youtu.be",
                    "ytimg.com",
                    "ggpht.com",
                    "googlevideo.com",
                    "youtube-nocookie.com",
                    "googleapis.com",
                    "yt.be",
                    "nhacuatui.com",
                    "google.com"
                    ],
                "outbound": "hideme"
            }
        ]

    }

}
'''
def get_hideme_addr_port():
    # adding hideme from sub64.txt 
    fl = open("sub64.txt")
    line = base64.b64decode (fl.read())   
    u = yarl.URL(line.decode())

    return u.host, u.port 
    
def main():
    config1 = json.loads(sys.stdin.read())
    config = json.loads(cfg)
    config['outbounds'] += config1['outbounds']
    
    hideme_data = get_hideme_addr_port()
    o1 = config['outbounds'][1]
    if o1['tag'] == 'hideme':
        config['outbounds'][1]['server'] = hideme_data[0]
        config['outbounds'][1]['server_port'] = hideme_data[1]
    else:
        raise RuntimeError("Check cfg format. tag hideme should be [1]") 
    print(json.dumps(config, indent=2))

if __name__ == "__main__": main()

