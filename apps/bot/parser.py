from .serialization import MessageSchema
import ujson


class Parser:
    def __init__(self, request):
        self.request = request
        self.data = self.serialization()

    def serialization(self):
        return MessageSchema().load(
            ujson.loads(self.request.body.decode('utf-8')))

    def chat_id(self):
        return self.data['message']['chat']['id']

    def text(self):
        return self.data['message']['text']
