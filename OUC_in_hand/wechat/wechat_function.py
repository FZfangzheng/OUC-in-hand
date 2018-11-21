import hashlib
import xmltodict
import time


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

    # 用于分辨信息类型，文本，图片等
    def classify(self):
        type = self.data.get("MsgType")
        if type == "text":
            return 1
        else:
            return 2
    # 文本信息功能回复
    def function_text_classify(self):
        if self.data.get("Content") == "课表":
            pass
        elif self.data.get("Content") == "成绩":
            pass
        elif self.data.get("Content") == "排名":
            pass
        elif self.data.get("Content") == "考场":
            pass
        elif self.data.get("Content") == "自习室":
            pass
        elif self.data.get("Content") == "给分情况":
            pass
        elif self.data.get("Content") == "错误报告":
            pass

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
