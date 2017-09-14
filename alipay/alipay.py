#-*- coding=utf-8 -*-
"""
支付宝登录获取订单信息脚本
ps.没啥卵用，使用selenium不稳定，经常出现问题。
使用前准备：
1.安装selenium：pip install selenium
2.下载webdriver。phantomjs无界面，适合linux；chromedriver方便调试。自定百度
3.修改USERNMAE和PASSWD

运行：
python alipay_login.py

pps. 脚本非原创。在v2ex一名v友的基础上修改的
"""
import requests
from selenium import webdriver
import time
import pickle
import re
requests.packages.urllib3.disable_warnings()

# 登录 url
Login_Url = 'https://auth.alipay.com/login/index.htm?goto=https://consumeprod.alipay.com/record/advanced.htm'
# 账单 url
Bill_Url = 'https://consumeprod.alipay.com/record/advanced.htm'
# 登录用户名和密码
USERNMAE = ''
PASSWD = ''
# 自定义 headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
    'Host': 'consumeprod.alipay.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}


class Alipay_Bill_Info(object):
    '''支付宝账单信息'''

    def __init__(self, headers, user, passwd):
        '''
        类的初始化
        headers：请求头
        cookies: 持久化访问
        info_list: 存储账单信息的列表
        '''
        self.headers = headers
        # 初始化用户名和密码
        self.user = user
        self.passwd = passwd
        # 利用 requests 库构造持久化请求
        self.session = requests.Session()
        # 将请求头添加到缓存之中
        self.session.headers = self.headers
        try:
            cookies = pickle.load(open("cookies", "rb"))
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            print u"获取cookies成功！"
        except:
            print u"未登陆过，需先登录"
            self.get_cookies()
        if not self.login_status():
            print u"cookies失效，重新登录"
            self.get_cookies()
        # 初始化存储列表
        self.info_list = []

    def wait_input(self, ele, str):
        '''减慢账号密码的输入速度'''
        for i in str:
            ele.send_keys(i)
            time.sleep(0.5)

    def get_cookies(self):
        '''获取 cookies'''
        # 初始化浏览器对象
        # sel = webdriver.PhantomJS(
        #    executable_path='C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
        # sel = webdriver.PhantomJS(
        #    executable_path='/root/phantomjs/bin/phantomjs')
        sel = webdriver.Chrome(executable_path='C:/chromedriver.exe')
        sel.maximize_window()
        sel.get(Login_Url)
        sel.implicitly_wait(3)
        # 找到用户名字输入框
        uname = sel.find_element_by_id('J-input-user')
        uname.clear()
        print u"正在输入账号....."
        self.wait_input(uname, self.user)
        time.sleep(1)
        # 找到密码输入框
        upass = sel.find_element_by_id('password_rsainput')
        upass.clear()
        print u"正在输入密码...."
        self.wait_input(upass, self.passwd)
        # 截图查看
        sel.save_screenshot('1.png')
        # 找到登录按钮
        button = sel.find_element_by_id('J-login-btn')
        time.sleep(1)
        print 1
        button.click()
        print 2
        sel.save_screenshot('2.png')
        if len(re.findall('checkSecurity', sel.current_url)) > 0:
            riskackcode = sel.find_element_by_id('riskackcode')
            riskackcode.clear()
            print u"等待输入验证码:"
            msgcode = raw_input()
            self.wait_input(riskackcode, msgcode)
            button = sel.find_element_by_xpath(
                '//*[@id="J-submit"]/input')  # ui-button
            time.sleep(1)
            button.click()
            sel.save_screenshot('2.1.png')
        print(sel.current_url)
        # 跳转到账单页面
        print u"正在跳转页面...."
        sel.get(Bill_Url)
        sel.implicitly_wait(3)
        sel.save_screenshot('3.png')
        # 获取 cookies 并转换为字典类型
        cookies = sel.get_cookies()
        pickle.dump(cookies, open("cookies", "wb"))
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        # 关闭浏览器
        sel.close()

    def set_cookies(self):
        '''将获取到的 cookies 加入 session'''
        self.get_cookies()

    def login_status(self):
        '''判断登录状态'''
        # 添加 cookies
        status = self.session.get(
            Bill_Url, timeout=5, allow_redirects=False, verify=False).status_code
        print(status)
        if status == 200:
            return True
        else:
            return False

    def get_data(self):
        '''
        利用 正则表达式解析 html
        并抓取数据，
        数据以字典格式保存在列表里
        '''
        status = self.login_status()
        if status:
            html = self.session.get(Bill_Url, verify=False).text
            # 抓取前五个交易记录
            trades = re.findall('<tr id="J-item-\d+?"[\w\W]*?</tr>', html)
            for trade in trades:
                # 做一个 try except 避免异常中断
                try:
                    # 分别找到账单的 时间 金额 以及流水号
                    day = re.findall(
                        '<p class="time-d">.*?(\d{4}\.\d{2}\.\d{2})', trade)[0]
                    time = re.findall(
                        '<p class="time-h ft-gray">.*?(\d{2}:\d{2})', trade)[0]
                    amount = re.findall(
                        '<span class="amount-pay">(.*?)</span> ', trade)[0]
                    ddh = re.findall(
                        '<td class="tradeNo ft-gray">.*?(\d{20})', trade)[0]  #
                    print day, time, amount, ddh
                except Exception, e:
                    print e
        else:
            print u"登录失败"


# test:
test = Alipay_Bill_Info(HEADERS, USERNMAE, PASSWD)
test.get_data()

