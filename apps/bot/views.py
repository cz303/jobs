from django.http import HttpResponse
from django.views import View
from bot.models.set_web_hook import SetWebHook
from bot.business_logic.menu import Menu

set_web_hook = SetWebHook()


class BotJobsView(View):

    def post(self, request):
        try:
            bot = set_web_hook.bot
            Menu(request=request, bot=bot).send()
        finally:
            return HttpResponse(status=200)
