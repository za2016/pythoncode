# coding:utf-8
import re
import requests as req

raw_cookies='' #cookies请自助获取
cookies={}
for line in raw_cookies.split(';'):
    key,value=line.split('=',1)
    cookies[key]=value

url='http://www.wndflb.com'
checkIn='http://www.wndflb.com/plugin.php?id=fx_checkin:checkin&formhash='

def qiandao(cookies):
    s=req.get(url,cookies=cookies)
    formhash=re.findall('checkin&formhash=(.*?)&',s.content)[0]
    urls=checkIn+formhash
    ss=req.get(urls,cookies=cookies)
    return ss

if __name__=='__main__':
    qiandao(cookies)
