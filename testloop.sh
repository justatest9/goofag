#!/usr/bin/bash

# testing proxies

#TEST_URL=http://speedtest.selectel.ru/100MB
TEST_URL=https://ash-speed.hetzner.com/100MB.bin

UUID_CONF=$(uuidgen).json
SOCKPORT=1085
RESULTS=tested.log

rm -f tested.log
curl -L -O https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/Base64/BLACK_VLESS_RUS_base64.txt
base64 -d BLACK_VLESS_RUS_base64.txt >BLACK_VLESS_RUS_base64_dec.txt
echo $TEST_URL $UUID
grep reality BLACK_VLESS_RUS_base64_dec.txt > BLACK_VLESS.txt
while read -r line; do
  python parset.py $line >$UUID_CONF
  echo $line
  cat $UUID_CONF
  ID=$(echo $line | cut -d'#' -f2)
  sing-box run -c $UUID_CONF &
  sleep 1
  (
    curl -o /dev/null -x socks5h://127.0.0.1:$SOCKPORT -m 10 -s -w '%{speed_download} ' $TEST_URL || true
    echo -n "$line "
    echo $ID
  ) >>$RESULTS
  pkill sing-box
  echo NEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
done <BLACK_VLESS.txt

## this is fixed naming top1..top5
# cat tested.log | sort -k1 -nr | grep -v United.*States | head -n 5 | cut -d' ' -f2 | cut -d'#' -f1 | awk '{print $0"#Top_"NR }' > topvless.txt

## instead using names from list
cat tested.log | sort -k1 -nr | grep -v United.*States | head -n 5 | cut -d' ' -f2  > topvless.txt

cat topvless.txt | base64  > topvless64.txt
