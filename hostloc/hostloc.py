#-*- coding=utf-8 -*-
import requests
import re 
import cookielib

index='http://www.hostloc.com/'
page_url='http://www.hostloc.com/forum-45-1.html'
login_url='http://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
login_data={
        'fastloginfield':'username'
        ,'username':''
        ,'cookietime':'2592000'
        ,'password':''
        ,'quickforward':'yes'
        ,'handlekey':'ls'
    }
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    ,'Accept-Encoding':'gzip, deflate, sdch'
    ,'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'
    ,'Host':'www.hostloc.com'
    ,'Referer':'http://www.hostloc.com/forum.php'
    ,'Upgrade-Insecure-Requests':'1'
    ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

class HostLoc():
    def __init__(self,username,passwd):
        self.username=username
        self.passwd=passwd
        login_data['username']=username
        login_data['password']=passwd
        self.session=requests.Session()
        self.session.headers=headers
        self.pass_jdkey()
        self.login()

    def pass_jdkey(self):
        html=self.session.get(index).content
        try:
            jdkey=re.findall('jdfwkey=(.*?)"')[0]
        except:
            jdkey=''
        url=index+'?jdfwkey='+jdkey
        self.session.get(index)
    
    def login(self):
        self.session.post(login_url,data=login_data)
    
    def isLogin(self):
        url='http://www.hostloc.com/home.php?mod=spacecp'
        html=self.session.get(url).content
        UserName=re.findall(self.username,html)
        if len(UserName)==0:
            return False
        else:
            return True
        
    def get_user(self):
        print('parse '+page_url)
        self.html=self.session.get(page_url).content
        user_pattern=re.compile('space-uid-\d+?.html')
        users=list(set(user_pattern.findall(self.html)))
        self.users=[index+i for i in users]

    def visit_user(self):
        for user in self.users[:10]:
            print('visit user '+user)
            self.session.get(user)
     

if __name__=='__main__':
    username='' #用户名
    passwd='' #密码
    hostloc=HostLoc(username,passwd)
    hostloc.get_user()
    hostloc.visit_user()
