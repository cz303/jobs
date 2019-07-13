from django.http import HttpResponse
from django.views import View
from bot.models.set_web_hook import SetWebHook
from bot.business_logic.menu import Menu
from .models.tables import User

set_web_hook = SetWebHook()


class BotJobsView(View):

    def post(self, request):
        bot = set_web_hook.bot
        try:
            Menu(request=request, bot=bot).send()
        except (User.DoesNotExist, AttributeError) as error:
            print(str(error))
            return HttpResponse(status=200)
        finally:
            return HttpResponse(status=200)
