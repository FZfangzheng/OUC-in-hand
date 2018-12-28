#-*- coding: utf-8 -*-
#filename:menu.py
import urllib.request, urllib.parse, urllib.error
from wechat.basic import  Basic

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print (urlResp.read())

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print (urlResp.read())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print (urlResp.read())

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print (urlResp.read())

if __name__=='__main__':
    myMenu=Menu()
    postJson="""
    {
        "button":[
        {
            "name":"教务查询",
            "sub_button":[
            {
                "type":"click",
                "name":"我的课表"
                "key":"课表"
            },
            {
                "type":"click",
                "name":"我的成绩"
                "key":"成绩"
            },
            {
                "type":"click"
                "name":"考试安排"
                "key":"考试安排"
            }]
        },
        {
            "name":"个人中心",
            "sub_button":[
            {
                "type":"click"
            "name":"绑定账号"
            "key":"绑定账号"
            }]
        }
        ]
    }
    """
    accessToken = Basic().get_access_token()
    myMenu.create(postJson,accessToken)
