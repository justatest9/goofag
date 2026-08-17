#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP

TOTAL_CHUNKS=30
CURPT=$(pwd)

cd $TMP
for ((i = 1; i <= $TOTAL_CHUNKS; i++)); do
  printf -v formi "%03d" "$i"
  curl -L -o "ebrasha$i.txt" "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/separated-protocols-chunks/vless/EbraSha-Protocol-Chunks-vless-$formi.txt"
done
cd $CURPT

echo File fetched

rm $TMP/TESTED_EBA.txt
for ((i = 1; i <= $TOTAL_CHUNKS; i++)); do
  grep reality "$TMP/ebrasha$i.txt" | bash $PTH/mttest/test.sh >>$TMP/TESTED_EBA.txt
done

#grep reality $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states' | grep -iv russia > $TMP/BLACK_VLESS.txt
#cat $TMP/BLACK_VLESS_RUS_base64_dec.txt | grep -iv 'united.*states'  > $TMP/BLACK_VLESS.txt

echo $PTH
cat $TMP/TESTED_EBA.txt | sort -r -n | cut -d \  -f 2- >$TMP/TESTED_EBA_CUT.txt
