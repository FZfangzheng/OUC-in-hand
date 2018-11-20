import hashlib


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
