#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import execjs
import hashlib
from functions import Functions
from functions.models import *


class Student:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__sessionid = ""
        self.__deskey = ""
        self.__nowtime = ""
        self.__url = self.getUrl(0)

    @staticmethod
    def getUrl(urlid):
        url = ['jwgl.ouc.edu.cn', 'jwgl2.ouc.edu.cn']
        return url[urlid]

    @property
    def sessionid(self):
        return self.__sessionid

    @sessionid.setter
    def sessionid(self, sessionid):
        self.__sessionid = sessionid

    @property
    def deskey(self):
        return self.__deskey

    @deskey.setter
    def deskey(self, deskey):
        self.__deskey = deskey

    @property
    def nowtime(self):
        return self.__nowtime

    @nowtime.setter
    def nowtime(self, nowtime):
        self.__nowtime = nowtime

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @staticmethod
    def encyptPassword(pwd):
        return hashlib.md5(pwd.encode("utf8")).hexdigest()

    def encyptUsername(self):
        try:
            content = """var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
            function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        out += base64EncodeChars.charAt(c1 >> 2);
        out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
        out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
        out += base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}"""
            s = requests.Session()
            sessionid = s.get("http://" + self.__url + "/cas/login.action", timeout=300).text.split("script", 7)[6].split('"', 5)[4]
            username = self.__username + ";;" + sessionid
            newusername = execjs.compile(content).call('base64encode', username)
            self.__sessionid = str(sessionid)
            return str(newusername)
        except:
            print("Error happened in encyptUsername()")
            return "", "", ""

    def getDeskeyAndNowtime(self):
        try:
            s = requests.Session()
            cookies = {'JSESSIONID': self.__sessionid}
            header = {
                'Host': self.__url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://' + self.__url + '/cas/login.action',
                'Connection': 'keep-alive'
            }
            SetKingoEncyptContent = s.get('http://' + self.__url + '/custom/js/SetKingoEncypt.jsp', headers=header,
                                          cookies=cookies, timeout=300)
            SetKingoEncyptContent.raise_for_status()
            content = SetKingoEncyptContent.text
            _deskey = content.split("\n", 4)[2].split("'", 3)[1]
            _nowtime = content.split("\n", 4)[3].split("'", 3)[1]
            self.__deskey = _deskey
            self.__nowtime = _nowtime
        except:
            print("Error happened in getDeskeyAndNowtime()")

    # 废弃
    # def getEncParams(self, params):
    #     try:
    #         self.getDeskeyAndNowtime()
    #         # deskey = "4021501230754998503"
    #         # nowtime = "2017-07-28 16:32:34"
    #         content = open("../SetKingo.js", 'r').read()
    #         # _params = execjs.compile(content).call('getEncParams',params,nowtime,deskey)
    #         _params = params
    #         return _params
    #     except:
    #         print("Error happened in getEncParams()")
    #         return "", "", ""

    def getAllInformation(self, openid):
        function = Functions.Function(self.__username, self.__url, self.__sessionid, self.__deskey, self.__nowtime)
        xn = "0000"
        xq = "0"
        informationlist = function.InquiryGrades(xn, xq, self.__username, xn + "-" + xq)
        exam_infor = function.examination()
        classInfor = function.myclass()
        for i in range(len(informationlist)):
            information = informationlist[i]
            grade = Grade(openid=openid, class_name=information[0], class_credit=information[1], class_grade=information[3])
            grade.save()
        for i in range(len(exam_infor)):
            information = exam_infor[i]
            exam = Exam(openid=openid, class_name=information[0], class_credit=information[1], class_type=information[2], class_way=information[3], class_time=information[4], class_location=information[5], class_seat=information[6])
            exam.save()

    def loginext(self, openid):
        randnumber = ""
        p_username = "_u" + randnumber
        p_password = "_p" + randnumber
        passwordPolicy = "1"
        password = str(self.encyptPassword(self.__password)) + str(self.encyptPassword(randnumber))
        password = str(self.encyptPassword(password))
        username = self.encyptUsername()
        params = p_username + "=" + username + "&" + p_password + "=" + password + "&randnumber=" + randnumber + "&isPasswordPolicy=" + passwordPolicy
        self.getDeskeyAndNowtime()
        _headers = {'Host': self.__url,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'Accept': 'text/plain, */*; q=0.01',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Origin': 'http: // ' + self.__url,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': 'http://' + self.__url + '/cas/login.action',
                    'Content-Length': '824',
                    'Cookie': 'JSESSIONID=' + self.__sessionid}
        postUrl = "http://" + self.__url + "/cas/logon.action"
        s = requests.session()
        s.headers.update(_headers)
        r = s.post(postUrl, data=params)
        if r.text == '{"message":"操作成功!","result":"\/MainFrm.html","status":"200"}':
            self.getAllInformation(openid)
            return True
        else:
            return False

