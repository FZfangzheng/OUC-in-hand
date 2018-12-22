import hashlib
import xmltodict
import time
from functions import User
from wechat.wechat_session import *
from functions.models import *

class WeChat:
    def __init__(self):
        pass

    @staticmethod
    def check_params(token, timestamp, nonce, signature):
        tmparr = [token, timestamp, nonce]
        tmparr.sort()
        tmpstr = ''.join(tmparr)
        tmpstr = hashlib.sha1(tmpstr.encode()).hexdigest()
        if tmpstr == signature:  # 验证成功，则返回True,否则返回false
            return True
        else:
            return False

    def handler(self, message):
        self.data = xmltodict.parse(message).get("xml")
        print("receive", self.data)
        return self.data

    # 用于分辨信息类型，文本，图片
    def classify(self):
        type = self.data.get("MsgType")
        if type == "text":
            return True
        else:
            return False

    # 文本信息功能回复
    def function_text_classify(self):
        if self.data.get("Content") == "绑定账号":
            # 绑定状态
            create_session(self.data.get("FromUserName"), "binding", 1)
            return "请输入账号"
        # 处在绑定账号状态
        if find_session(self.data.get("FromUserName"), "binding") == "1":
            if len(Users.objects.filter(user=self.data.get("Content"))) == 0:
                create_session(self.data.get("FromUserName"), "username", self.data.get("Content"))
                # 输入密码状态
                change_session(self.data.get("FromUserName"), "binding", 2)
                return "请输入密码"
            else:
                del_session(self.data.get("FromUserName"), "username")
                del_session(self.data.get("FromUserName"), "binding")
                return "该账号已被注册"
        # 绑定密码状态
        if find_session(self.data.get("FromUserName"), "binding") == "2":
            usr = find_session(self.data.get("FromUserName"), "username")
            pwd = self.data.get("Content")
            user = User.Student(usr, pwd)
            # 登陆成功
            if user.loginext(self.data.get("FromUserName")):
                us = Users(openid=self.data.get("FromUserName"), user=usr, pwd=pwd)
                us.save()
                # 清空session
                del_session(self.data.get("FromUserName"), "binding")
                del_session(self.data.get("FromUserName"), "username")
                return "绑定成功！"
            else:
                # 清空session
                del_session(self.data.get("FromUserName"), "binding")
                del_session(self.data.get("FromUserName"), "username")
                return "绑定失败！"
        if self.data.get("Content") == "课表":
            pass
        elif self.data.get("Content") == "成绩":
            return self.grade()
        elif self.data.get("Content") == "考试安排":
            return self.exam()
        else:
            return "输入特定关键字使用功能\n1.绑定账号\n2.课表\n3.成绩\n4.考试安排"

    def exam(self):
        myExam = Exam.objects.filter(openid=self.data.get("FromUserName"))
        grade = "名称\t学分\t类型\t方式\t时间\t教室\t座位\n"
        for e in myExam:
            grade = grade+e.class_name+"\t"+e.class_credit+"\t"+e.class_type+"\t"+e.class_way+"\t"+e.class_time+"\t"+e.class_location+"\t"+e.class_seat+"\n"
        return grade

    def grade(self):
        myGrade=Grade.objects.filter(openid=self.data.get("FromUserName"))
        grade="课程名称\t课程学分\t分数\n"
        for g in myGrade:
            grade = grade+g.class_name+"\t"+g.class_credit+"\t"+g.class_grade+"\n"
        return grade
    def reply_text(self, content):
        template = """<xml>
                <ToUserName>{}</ToUserName>
                <FromUserName>{}</FromUserName>
                <CreateTime>{}</CreateTime>
                <MsgType>{}</MsgType>
                <Content>{}</Content>
                </xml>"""

        result = template.format(self.data["FromUserName"], self.data["ToUserName"], int(time.time()), "text", content)
        print(result)
        return result
