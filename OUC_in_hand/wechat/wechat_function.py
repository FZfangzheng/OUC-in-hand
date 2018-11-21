import hashlib
import xmltodict
import time
from functions import User
from wechat.wechat_session import *

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
        if find_session(self.data.get("FromUserName"), "binding1") == 1:
            create_session(self.data.get("FromUserName"), "username", self.data.get("Content"))
            # 输入密码状态
            change_session(self.data.get("FromUserName"), "binding", 2)
            return "请输入密码"
        # 绑定密码状态
        if find_session(self.data.get("FromUserName"), "binding") == 2:
            usr = find_session(self.data.get("FromUserName"), "username")
            pwd = self.data.get("Content")
            user = User.Student(usr, pwd)
            # 清空session
            del_session(self.data.get("FromUserName"), "binding")
            del_session(self.data.get("FromUserName"), "username")
            if user.loginext():
                return "绑定成功！"
            else:
                return "绑定失败！"
        if self.data.get("Content") == "课表":
            pass
        elif self.data.get("Content") == "成绩":
            pass
        elif self.data.get("Content") == "考试安排":
            pass
        else:
            return "输入特定关键字使用功能\n1.绑定账号\n2.课表\n3.成绩\n4.考试安排"

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
