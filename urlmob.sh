#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP

CURPT=$(pwd)
cd $TMP
curl -L -O -s https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt
curl -L -o ebrasha1.txt https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols-chunks/vless/EbraSha-Protocol-Chunks-vless-001.txt
curl -L -o ebrasha2.txt https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols-chunks/vless/EbraSha-Protocol-Chunks-vless-002.txt
curl -L -o ebrasha3.txt https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols-chunks/vless/EbraSha-Protocol-Chunks-vless-003.txt
curl -L -o ebrasha4.txt https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols-chunks/vless/EbraSha-Protocol-Chunks-vless-004.txt
cd $CURPT

base64 -d $TMP/BLACK_VLESS_RUS_base64.txt >$TMP/BLACK_VLESS_RUS_base64_dec.txt

rm $TMP/BLACK_VLESS.txt
grep reality $TMP/ebrasha1.txt >>$TMP/BLACK_VLESS.txt
grep reality $TMP/ebrasha2.txt >>$TMP/BLACK_VLESS.txt
grep reality $TMP/ebrasha3.txt >>$TMP/BLACK_VLESS.txt
grep reality $TMP/ebrasha4.txt >>$TMP/BLACK_VLESS.txt
#grep . $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia >$TMP/BLACK_VLESS.txt
#grep reality $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia >$TMP/BLACK_VLESS.txt

echo $PTH
cat $TMP/BLACK_VLESS.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox1.json
