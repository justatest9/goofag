#!/bin/bash

# parameters $1 - id
# stdin - url (vless://....)
#
TEST_URL=https://ash-speed.hetzner.com/100MB.bin
STARTING_PORT=20000
TMP=/tmp/singtest
ID=$1
CFG_FILE="$TMP/testcfg_id$ID.json"
RES_FILE="$TMP/results_id$ID.txt"
PORT=$(($STARTING_PORT + $ID))

PTH=$(dirname $0)

if [[ -z "$ID" ]]; then
  echo empty id
  exit 1
fi
read PROXY_URL

#echo $PORT
python $PTH/../parset.py "$PROXY_URL" $PORT >$CFG_FILE

sing-box run -c "$CFG_FILE" &
SINGBOX_PID=$!
#echo pid $SINGBOX_PID
sleep 1
# now run curl
#
(
  curl -o /dev/null -x socks5h://127.0.0.1:$PORT -m 10 -w '%{speed_download} ' $TEST_URL || true
  echo -n "$ID "
  echo $PROXY_URL
) >$RES_FILE

kill $SINGBOX_PID
#pause
#cat $CFG_FILE
rm $CFG_FILE
