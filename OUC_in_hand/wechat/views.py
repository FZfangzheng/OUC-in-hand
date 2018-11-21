from django.shortcuts import render
from django.http import HttpResponse
from wechat import wechat_function
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def index(request):
    # 初次认证
    if request.method == "GET":
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        if wechat_function.WeChat.check_params("OUC_in_hand_16020031016", timestamp, nonce, signature):
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")
    # 之后信息请求
    elif request.method == "POST":
        wechat = wechat_function.WeChat()
        wechat.handler(request.body)
        return HttpResponse(wechat.reply_text(wechat.data.get("Content")))

