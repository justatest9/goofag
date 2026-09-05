#!/bin/bash

# stdin - full proxy list for testing
# stdout - list of (speed; url)
#
TMP=/tmp/singtest
PTH=$(dirname $0)
ID=0

CFG_FILE="$TMP/testcfg_full.json"
STARTING_PORT=20000

# making single singbox config
FULL_INPUT=$(cat)
echo "$FULL_INPUT" | python $PTH/../parset.py $STARTING_PORT >$CFG_FILE

sing-box run -c "$CFG_FILE" &
SINGBOX_PID=$!
sleep 1

pidar=()
while read -r line; do
  RES=$(echo $line | python $PTH/../parset.py 0)
  if [ "$RES" = "{}" ]; then continue; fi
  echo $line | bash $PTH/thread.sh $ID &
  pidar+=($!)
  #echo $line $ID $RES
  #python $PTH/../parset.py "$line"$PORT >$CFG_TMPL{ID}.json
  ID=$(($ID + 1))
done <<<"$FULL_INPUT"

if [ "${#pidar[@]}" -gt 0 ]; then
  echo "waiting started ${pidar[@]}" >&2
  wait "${pidar[@]}"
fi

kill $SINGBOX_PID

for res_file in $TMP/results_id*; do
  read -r speed id url <$res_file
  if [ "$speed" -gt 1 ]; then
    echo $speed $url
  fi
  #rm $res_file
done
