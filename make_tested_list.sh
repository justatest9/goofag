#!/bin/sh

PTH=$(dirname $0)
TMP=/tmp/singtest
#export https_proxy="192.168.88.1:8080"

(
  #sh ftch.sh https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols/hysteria2_configs.txt
  sh ftch.sh https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt
  #cat $PTH/exhaust/fixed_list.txt
  # ebrasha vless full
  sh ftch.sh https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols/vless_configs.txt | grep reality
) |
  python remove_duplicates.py |
  bash $PTH/mttest/test.sh |
  cut -d\  -f 2- >$PTH/exhaust/tested_list.txt

exit
bash $PTH/ebrasha_autosel.sh
cat $TMP/TESTED_EBA_CUT.txt >>$PTH/exhaust/tested_list.txt
