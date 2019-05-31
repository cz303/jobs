from django.http import HttpResponse
from django.views import View
from .set_web_hook import SetWebHook
from .dialog import Dialog

set_web_hook = SetWebHook()


class BotJobsView(View):
    def post(self, request):
        bot = set_web_hook.bot
        Dialog(request=request, bot=bot).send()
        return HttpResponse(status=200)
