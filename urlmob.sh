#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP

CURPT=$(pwd)
cd $TMP
curl -L -O -s https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt
cd $CURPT

base64 -d $TMP/BLACK_VLESS_RUS_base64.txt >$TMP/BLACK_VLESS_RUS_base64_dec.txt

grep . $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia >$TMP/BLACK_VLESS.txt
#grep reality $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia >$TMP/BLACK_VLESS.txt

#bash ebrasha_autosel.sh
#bash ebr_auto_hyst.sh

echo $PTH
#cat $TMP/BLACK_VLESS.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox1.json
cat $TMP/TESTED_EBA_HYST_CUT.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox2.json

# for now just take fixed list and prepare config
cat exhaust/fixed_list.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox1.json
