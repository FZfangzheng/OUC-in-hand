from django.shortcuts import render
from django.http import HttpResponse
from wechat import wechat_function
# Create your views here.


def index(request):
    if request.method == "GET":

        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        if wechat_function.WeChat.check_params("OUC_in_hand_16020031016", timestamp, nonce, signature):
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")