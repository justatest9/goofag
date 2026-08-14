#!/bin/bash

for ((i = 0; i < 3; i++)); do
  vers=$(curl -s https://api.github.com/repos/SagerNet/sing-box/releases |
    grep tag_name | grep -v beta | head -n 1 | awk -F: '{print $2}' | sed 's/[", v]//g')
  if [[ ! -z "$vers" ]]; then break; fi
done

echo $vers

curl -v -o pack.deb -L https://github.com/SagerNet/sing-box/releases/download/v$vers/sing-box_''$vers''_linux_amd64.deb

sudo apt install ./pack.deb
