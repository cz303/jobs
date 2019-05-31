import ujson
from pprint import pprint
from django.http import HttpResponse
from django.views import View
from .bot import Bot
from .serialization import MessageSchema


class BotJobsView(View):
    def post(self, request):
        bot = Bot().bot
        schema = MessageSchema()
        data = schema.load(ujson.loads(request.body.decode('utf-8')))
        pprint(data)

        user_id = data['message']['user']['id']
        bot.send_message(chat_id=user_id, text='ok')

        return HttpResponse(status=200)
