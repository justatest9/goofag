#!/bin/env/python

# this bitch takes v2ray list in stdin
#
import yarl
import sys
import json
import urllib.parse

def subs(ard, keyd, ars, keys):
    if keys in ars.keys(): ard[keyd] = ars[keys]

# parse line to outbound map
def parseline(line):
    u = yarl.URL(line)
    
    # making singbox vless outbound array
    vless_outbound = {}
    vless_outbound['type'] = 'vless'
    vless_outbound['tag'] = urllib.parse.unquote(line.split('#')[1])
    vless_outbound['server'] = u.host 
    vless_outbound['server_port'] = u.port
    vless_outbound['uuid'] = u.user

    subs(vless_outbound, 'flow', u.query, 'flow')
    subs(vless_outbound, 'packet_encoding', u.query, 'packetEncoding')

    
    tls = {}
    utls = {}
    reality = {}
    sec = u.query['security'] if 'security' in u.query.keys() else 'none'

    vless_outbound['tls'] = tls
    
    if 'fp' in u.query.keys() or sec == 'reality':
        tls['utls'] = utls
        utls['enabled'] = True
        utls['fingerprint'] = ''

    subs(utls, 'fingerprint', u.query, 'fp')
        
    if sec == 'reality': 
        tls['reality'] = reality
        reality['enabled'] = True
        subs(reality, 'public_key', u.query, 'pbk')
        subs(reality, 'short_id', u.query, 'sid')

    if sec != 'none': 
        tls['enabled'] = True
        if 'sni' in u.query.keys(): tls['server_name'] = u.query['sni'] 

    return vless_outbound

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
