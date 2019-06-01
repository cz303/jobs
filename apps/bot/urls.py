from django.urls import path
from bot.views import BotJobsView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('{}'.format(settings.TOKEN), csrf_exempt(BotJobsView.as_view()),
         name='bot_view'),
]
