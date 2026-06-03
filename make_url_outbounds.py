#!/bin/env/python

# this bitch takes v2ray list in stdin
#
import yarl
import sys
import json
import urllib.parse
from parset import parseline

def subs(ard, keyd, ars, keys):
    if keys in ars.keys(): ard[keyd] = ars[keys]

def kill_dupes(olist):
    reslist = []
    for o in olist:
        dup_found = False
        for rs in reslist:
            if o['server'] == rs['server'] and o['server_port'] == rs['server_port'] and \
                o['uuid'] == rs['uuid']:
                # this is dup
                dup_found = True
                break
        if not dup_found: reslist.append(o)
    return reslist

def main():
  
    outbounds = []
    for line in sys.stdin:
        cline = line.strip()
        outbounds.append(parseline(cline))

    #print(outbounds)
    print('Initial len: ', len(outbounds), end='', file=sys.stderr)
    outbounds = kill_dupes(outbounds)
    print(' deduplicated len: ', len(outbounds), file=sys.stderr)

    for i in range(len(outbounds)):
        outbounds[i]['tag'] += ' #' + str(i)
        outbounds[i]['connect_timeout'] = '3s'
    # making config
    
    urltest_o = {}
    urltest_o['type'] ='urltest'
    urltest_o['tag'] ='autosel'
    urltest_o['outbounds'] = [i['tag'] for i in outbounds]

    urltest_o['url'] = 'https://cp.cloudflare.com'
    urltest_o['interval'] = '1m'
    urltest_o['tolerance'] = 100
    urltest_o['idle_timeout'] = '30m'
    urltest_o['interrupt_exist_connections'] = False
    outbounds = [urltest_o] + outbounds
    

    config = {}
    config['outbounds'] = outbounds
    
    dmp = json.dumps(config, indent=2)   
    print(dmp)

if __name__ == "__main__": main()
