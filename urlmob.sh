#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP

CURPT=$(pwd)
cd $TMP
curl -L -O -s https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt
cd $CURPT

base64 -d $TMP/BLACK_VLESS_RUS_base64.txt >$TMP/BLACK_VLESS_RUS_base64_dec.txt
grep reality $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states'  > $TMP/BLACK_VLESS.txt

echo $PTH
cat $TMP/BLACK_VLESS.txt | python $PTH/make_url_outbounds.py >$PTH/urlmob.json

