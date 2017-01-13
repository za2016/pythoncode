#-*- coding=utf-8 -*-
import requests
import json
import sys

tc_api='https://sm.ms/api/upload'
files={
    'smfile':''
    }
data={'ssl':'false'
    ,'format':'json'}

def smms(filepath):
    try:
        img=open(filepath,'rb')
    except Exception,e:
        print e
        sys.exit(0)
    files['smfile']=img
    c=requests.post(tc_api,files=files,data=data)
    dat=json.loads(c.content)
    if dat['code']=='error':
        img=dat['msg']
    if dat['code']=='success':
        img=dat['data']['url']
    return img