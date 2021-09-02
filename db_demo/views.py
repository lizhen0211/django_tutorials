from time import sleep

# Create your views here.
from django.views.generic.base import View

from db_demo.models import Question, Choice
from utils.responses import HttpJsonResponse


class DBConnectionReleaseView(View):
    """
    查看所有连接的用户
    select * from pg_stat_activity;

    查看连接总数
    select count(*) from pg_stat_activity;
    """

    def get(self, request):
        # 接口方法不返回，数据库连接不释放
        choicies_qs = Choice.objects.filter()
        print(choicies_qs)
        questions_qs = Question.objects.filter()
        print(questions_qs)
        sleep(10)
        return HttpJsonResponse(status=200)
