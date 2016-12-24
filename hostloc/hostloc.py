#-*- coding=utf-8 -*-
import requests
import re 
import cookielib
import sys

index='http://www.hostloc.com/'
page_url='http://www.hostloc.com/forum-45-1.html'
credit_url='http://www.hostloc.com/home.php?mod=spacecp&ac=credit&showcredit=1'
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
        self.login()
        self.pass_jdkey()
        

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

    def get_credit(self):
        html=self.session.get(credit_url).content
        credit_pattern=re.compile(r'</ul><ul class="creditl mtm bbda cl"><li class="xi1 cl"><em> 金钱: </em>(.*?)  .*? </li>[\w\W]*?<li><em> 威望: </em>(.*?) </li>[\w\W]*?<li class="cl"><em>积分: </em>(.*?) <span class="xg1">')
        try:
            credit=credit_pattern.findall(html)
            coin,wh,jf=credit[0]
            print u"金币：%s，威望：%s，积分：%s"%(coin,wh,jf)
            return True
        except:
            print u"获取数据失败，请稍后再试"
            return False
        
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
    if hostloc.get_credit():
        hostloc.get_user()
        hostloc.visit_user()
        hostloc.get_credit()
    else:
        sys.exit(0)
