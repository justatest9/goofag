#!/bin/bash

# parameters $1 - id
# stdin - url (vless://....)
#
TEST_URL=https://ash-speed.hetzner.com/100MB.bin
PING_TIMEOUT=5
STARTING_PORT=20000
TMP=/tmp/singtest
ID=$1
RES_FILE="$TMP/results_id$ID.txt"
PORT=$(($STARTING_PORT + $ID))

PTH=$(dirname $0)

if [[ -z "$ID" ]]; then
  echo empty id
  exit 1
fi
read PROXY_URL

#echo $PORT

# now lets try udp
for ((i = 0; i < 3; i++)); do
  python $PTH/udp_echo.py -w $PING_TIMEOUT -p 127.0.0.1 -P $PORT 1>&2
  UDPSTATUS=$((!$?))
  if (($UDPSTATUS)); then break; fi
done

echo udp test done! status $UDPSTATUS >&2

TGSTATUS=0
if (($UDPSTATUS)); then
  # lets try telegram connectivity
  for ((i = 0; i < 3; i++)); do
    TGSTATUS=$(curl -IL -m 10 -x socks5h://127.0.0.1:$PORT https://api.telegram.org | grep -q 'HTTP.*200' && echo 1 || echo 0)
    if (($TGSTATUS)); then break; fi
    sleep 1
  done
  echo Telegram status: $TGSTATUS >&2
fi

# now run curl to test speed
#
if (($UDPSTATUS && $TGSTATUS)); then
  SPEED=$(curl -o /dev/null -x socks5h://127.0.0.1:$PORT -m 10 -w '%{speed_download} ' $TEST_URL)
fi

#(
#  true ||
#  curl -o /dev/null -x socks5h://127.0.0.1:$PORT -m 10 -w '%{speed_download} ' $TEST_URL || true
#  echo -n "$ID "
#  echo $PROXY_URL
#) >$RES_FILE

RESULT=$(($TGSTATUS && $UDPSTATUS))
if (($RESULT)); then RESULT=$SPEED; fi

echo $RESULT $ID $PROXY_URL >$RES_FILE
