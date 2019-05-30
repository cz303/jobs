import ujson
from pprint import pprint
from django.http import HttpResponse
from django.views import View


class BotJobsView(View):
    def post(self, request):
        data = ujson.loads(request.body.decode('utf-8'))
        pprint(data)
        return HttpResponse(status=200)
