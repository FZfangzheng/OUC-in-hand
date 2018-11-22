from wechat.models import MySession


def create_session(openid, name, content):
    mysession = MySession(openid=openid, wechat_session=name, session_value=content)
    mysession.save()


def del_session(openid, name):
    mysessions = MySession.objects.filter(openid=openid).filter(wechat_session=name)
    if len(mysessions) == 0:
        return False
    else:
        mysessions[0].delete()
        return True


def change_session(openid, name, content):
    MySession.objects.filter(openid=openid).filter(wechat_session=name).update(session_value=content)


def isExist(openid, name):
    mysessions = MySession.objects.filter(openid=openid).filter(wechat_session=name)
    if len(mysessions) == 0:
        return False
    else:
        return True


def find_session(openid, name):
    mysessions = MySession.objects.filter(openid=openid).filter(wechat_session=name)
    if len(mysessions) == 0:
        return ""
    else:
        return mysessions[0].session_value
