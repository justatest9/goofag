#!/bin/env/python

import json
import urllib.request
from datetime import datetime
import base64


pref_array = ('Switzerland', 'Netherlands')
instance_name = 'hideme_github'

class logger:
    def __init__(self):
        self.f = open('log.txt', 'a')

        
    def w(self, txt):
        self.f.write(str(datetime.now()) + ' ' + txt + '\n')
    def __del__(self):
        self.f.close()

log = logger()


url = "http://188.166.142.39/servers/list"

try:
    r = urllib.request.urlopen(url)
    data = json.loads(r.read())
    print(data)

    found = False
    rec = None
    for loc in pref_array:
        for i in data:
            if i['name'] == loc:
                found = True
                rec = i
                break
        if found: break
    
    log.w('Updating to: ' + str(rec))
    
    buf = f"socks://{rec['host']}:{rec['port']}#{instance_name}"
    basetxt = base64.b64encode(buf.encode())

    f = open('sub64.txt', 'w')
    f.write(basetxt.decode())
    f.close()

except Exception as e:
    log.w('Наебнулось ' + str(e.with_traceback(None)))

