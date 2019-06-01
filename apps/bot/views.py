from django.http import HttpResponse
from django.views import View
from bot.set_web_hook import SetWebHook
from bot.menu import Menu

set_web_hook = SetWebHook()


class BotJobsView(View):
    def post(self, request):
        bot = set_web_hook.bot
        Menu(request=request, bot=bot).send()
        return HttpResponse(status=200)
