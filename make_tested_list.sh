#!/bin/sh

PTH=$(dirname $0)
TMP=/tmp/singtest

(
  sh ftch.sh https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols/hysteria2_configs.txt
  sh ftch.sh https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt | base64 -d
) |
  python remove_duplicates.py |
  bash $PTH/mttest/test.sh |
  cut -d\  -f 2- >$PTH/exhaust/tested_list.txt
