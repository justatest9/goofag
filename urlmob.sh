#!/usr/bin/bash

PTH=$(dirname $0)
TMP=/tmp/singtest

mkdir -p $TMP


#bash ebrasha_autosel.sh
#bash ebr_auto_hyst.sh

echo $PTH
#cat $TMP/BLACK_VLESS.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox1.json
( 
  cat $PTH/exhaust/fixed_list.txt ;
  cat $PTH/exhaust/tested_list.txt
) | 
  python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox2.json

# for now just take fixed list and prepare config
#cat exhaust/fixed_list.txt | python $PTH/make_url_outbounds.py | python append_to_singbox_config.py >$PTH/singbox1.json
