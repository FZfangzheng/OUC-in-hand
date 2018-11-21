from wechat.models import MySession


def create_session(openid, name, content):
    mysession = MySession(openid=openid, wechat_session=name, session_value=content)
    mysession.save()


def del_session(openid, name):
    if len(MySession.objects.filter(openid=openid)) == 0:
        return False
    else:
        mysession = MySession.objects.filter(openid=openid).get(wechat_session=name)
        mysession.delete()
        return True


def change_session(openid, name, content):
    mysession = MySession.objects.filter(openid=openid).get(wechat_session=name)
    mysession.session_value = content
    mysession.save()


def isExist(openid, name):
    if len(MySession.objects.filter(openid=openid)) == 0:
        return False
    else:
        mysession = MySession.objects.filter(openid=openid).get(wechat_session=name)
        if mysession != 0:
            return True
        else:
            return True


def find_session(openid, name):
    if len(MySession.objects.filter(openid=openid)) == 0:
        return ""
    else:
        mysession = MySession.objects.filter(openid=openid).get(wechat_session=name)
        if len(mysession) == 0:
            return ""
        else:
            return mysession.session_value
