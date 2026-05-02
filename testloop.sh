#!/usr/bin/bash

# testing proxies

#TEST_URL=http://speedtest.selectel.ru/100MB
TEST_URL=https://ash-speed.hetzner.com/100MB.bin

UUID_CONF=$(uuidgen).json
SOCKPORT=1085
RESULTS=tested.log

rm tested.log
curl https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt
base64 -d BLACK_VLESS_RUS_base64.txt >BLACK_VLESS_RUS_base64_dec.txt
echo $TEST_URL $UUID
while read -r line; do
  python parset.py $line >$UUID_CONF
  ID=$(echo $line | cut -d'#' -f2)
  sing-box run -c $UUID_CONF &
  sleep 1
  (
    curl -o /dev/null -x socks5h://127.0.0.1:$SOCKPORT -m 10 -s -w '%{speed_download} ' $TEST_URL
    echo -n "$line "
    echo $ID
  ) >>$RESULTS
  kill $!
  echo NEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
done <BLACK_VLESS_RUS_base64_dec.txt
