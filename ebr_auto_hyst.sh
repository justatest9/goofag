#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP

CURPT=$(pwd)

cd $TMP
curl -L -o ebrasha_hyst.txt https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols/hysteria2_configs.txt
cd $CURPT

echo File fetched

rm $TMP/TESTED_EBA_HYST.txt
cat $TMP/ebrasha_hyst.txt | bash $PTH/mttest/test.sh >>$TMP/TESTED_EBA_HYST.txt

#grep reality $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia > $TMP/BLACK_VLESS.txt
#cat $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states'  > $TMP/BLACK_VLESS.txt

echo $PTH
cat $TMP/TESTED_EBA_HYST.txt | cut -d \  -f 2- >$TMP/TESTED_EBA_HYST_CUT.txt
