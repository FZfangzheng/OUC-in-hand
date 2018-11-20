from django.shortcuts import render

# Create your views here.
import hashlib
from django.http import HttpResponse


def check_params(token, timestamp, nonce, signature):
    tmparr = [token, timestamp, nonce]
    tmparr.sort()
    tmpstr = ''.join(tmparr)
    tmpstr = hashlib.sha1(tmpstr.encode()).hexdigest()
    if tmpstr == signature:  # 验证成功，则返回True,否则返回false
        return True
    else:
        return False


def check(request):
    if request.method == "GET":

        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        if check_params("OUC_in_hand_16020031016", timestamp, nonce, signature):
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")









