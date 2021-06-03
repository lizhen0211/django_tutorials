# Create your views here.
from django.views.generic.base import View

from utils.responses import HttpJsonResponse


class SetCookieView(View):

    def get(self, request):
        response = HttpJsonResponse("", status=200)
        # request url 请求域名（xxx.lizhen.com）和Response Headers中Set-Cookie中的Domain（lizhen.com）需要匹配
        # 否则 浏览器的response中 set-cookie里可以看到值，但是浏览器的 Application中Cookies中不能写入cookie
        response.set_cookie('hello', 'django', expires=60 * 60 * 24 * 7, secure=False, domain='lizhen.cn')
        return response


class DeleteCookieView(View):

    def delete(self, request):
        response = HttpJsonResponse(status=204)
        response.delete_cookie('hello')
        return response
