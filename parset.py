#!/bin/env/python

# this bitch parses a vless url line (argv[1]) to config.json for sing-box (stdout)
# check out $? return status for 0 if ok

import yarl
import sys
import json
import urllib.parse
import subprocess
import os


tmp_file="/tmp/singtest/c" + str(os.getpid()) +".json"

def err(str):
    print(str, file=sys.stderr)

def validate_singbox_config(outbnd):
    conf = {}
    conf['outbounds'] = []
    conf['outbounds'].append(outbnd)
    # err(conf)
    ftmp_file = open(tmp_file, mode="w")
    print(json.dumps(conf, indent=2), file=ftmp_file)
    ftmp_file.close()
    res = subprocess.run(["sing-box", "check", "-c", tmp_file], stdout=subprocess.DEVNULL)
    os.remove(tmp_file)
    if res.returncode == 0:
        return True
    return False

def parseline_vless(url):

    u = url
     # making singbox vless outbound array
    vless_outbound = {}
    vless_outbound['type'] = 'vless'
    vless_outbound['tag'] = u.fragment
    vless_outbound['server'] = u.host 
    vless_outbound['server_port'] = u.port
    vless_outbound['uuid'] = u.user

    subs(vless_outbound, 'flow', u.query, 'flow')
    #subs(vless_outbound, 'packet_encoding', u.query, 'packetEncoding')

    tls = {}
    utls = {}
    reality = {}
    sec = u.query['security'] if 'security' in u.query.keys() else 'none'

    vless_outbound['tls'] = tls
    
    if 'fp' in u.query.keys() or sec == 'reality':
        tls['utls'] = utls
        utls['enabled'] = True
        utls['fingerprint'] = ''
        tls['enabled'] = True

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

def parseline_hysteria2(url):
    
    hyst_outbound = {}
    hyst_outbound['type'] = 'hysteria2'
    hyst_outbound['tag'] = url.fragment
    hyst_outbound['server'] = url.host 
    hyst_outbound['server_port'] = url.port
    hyst_outbound['password'] = url.user
    
    hyst_outbound['up_mbps'] = 20
    hyst_outbound['down_mbps'] = 20

    tls = {}
    utls = {}
    obfs = {}
    tls['enabled'] = True
    
    subs(tls, 'server_name', url.query, 'sni')
    
    if 'insecure' in url.query.keys():
        insec = url.query['insecure']
        tls['insecure'] = bool(insec)
    
    if 'obfs' in url.query.keys():
        obfs['type'] = url.query['obfs']
        obfs['password'] = url.query['obfs-password']
    
    if 'fp' in url.query.keys():
        tls['utls'] = utls
        utls['enabled'] = True
        utls['fingerprint'] = url.query['fp']

    hyst_outbound['tls'] = tls
    hyst_outbound['obfs'] = obfs
    return hyst_outbound

def parseline(line):
    u = yarl.URL(line)
    
    if(u.scheme == 'vless'):
        outbound = parseline_vless(u)
    elif(u.scheme == 'hysteria2'):
        outbound = parseline_hysteria2(u)
    else:
        return {}

    if validate_singbox_config(outbound):
        return outbound
    return {}

def subs(ard, keyd, ars, keys):
    if keys in ars.keys(): ard[keyd] = ars[keys]

# dumps singbox testing config to stdout
# $1  - port
def main():

    argc = len(sys.argv)
    argv = sys.argv
    lport = 1085 
    if argc>2: 
        lport = int(argv[2])
    
    sing_outbound = parseline(argv[1])
    sing_outbound['tag'] = 'proxy'

    local_inbound = {}
    local_inbound['type'] = 'socks'
    local_inbound['tag'] = 'in'
    local_inbound['listen'] = '127.0.0.1'
    local_inbound['listen_port'] = lport

    config = {}
    config['outbounds'] = [sing_outbound]
    config['inbounds'] = [local_inbound]
    route = {}
    rules = []
    config['route'] = route
    route['rules'] = rules
    rule = {}
    rule['inbound'] = 'in'
    rule['outbound'] = 'proxy'
    rules.append(rule)

    dmp = json.dumps(config, indent=2)   

    print(dmp)

if __name__ == "__main__": main()
#vless://b25b7433-e364-499c-b583-15b277783385@alban.helper-internet.com:443?type=tcp&headerType=none&security=reality&encryption=none&sni=alban.helper-internet.com&fp=random&pbk=W-zf_ncm9sYALF5EqvUsxqTkYGdAw-tQczT2SqwVMGE&sid=ff776ff77be48b88&spx=%2F&flow=xtls-rprx-vision#%F0%9F%87%A6%F0%9F%87%B1%20Albania%2C%20Tirana%20%7C%20%F0%9F%8C%90%20%7C%20%5BIPv6%5D%20%7C%20%5BBL%5DЖ
