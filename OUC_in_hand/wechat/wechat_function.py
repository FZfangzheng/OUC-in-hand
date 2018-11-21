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

    def reply(self, content):
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