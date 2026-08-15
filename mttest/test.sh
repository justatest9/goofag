#!/bin/bash

# stdin - full proxy list for testing
# stdout - list of (speed; url)
#
TMP=/tmp/singtest
PTH=$(dirname $0)
ID=0

pidar=()

while read -r line; do
  echo $line | bash $PTH/thread.sh $ID &
  ID=$(($ID + 1))
  pidar+=($!)
done

wait ${pidar[@]}

for res_file in $TMP/results_id*; do
  read -r speed id url <$res_file
  if [ "$speed" -gt 10 ]; then
    echo $speed $url
  fi
  rm $res_file
done
