#!/bin/env/python

# this bitch parses a vless url line (argv[1]) to config.json for sing-box (stdout)
# check out $? return status for 0 if ok

import yarl
import sys
import json

def subs(ard, keyd, ars, keys):
    if keys in ars.keys(): ard[keyd] = ars[keys]

def main():

    argc = len(sys.argv)
    argv = sys.argv
    u = yarl.URL(argv[1])

    # making singbox vless outbound array
    vless_outbound = {}
    vless_outbound['type'] = 'vless'
    vless_outbound['tag'] = 'proxy'
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

    local_inbound = {}
    local_inbound['type'] = 'socks'
    local_inbound['tag'] = 'in'
    local_inbound['listen'] = '127.0.0.1'
    local_inbound['listen_port'] = 1085

    config = {}
    config['outbounds'] = [vless_outbound]
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
