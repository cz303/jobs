from bot.serialization import MessageSchema
import ujson


class Parser:
    def __init__(self, request):
        self.request = request
        self.schema = MessageSchema()
        self.json = ujson
        self.data = self.serialization()

    def serialization(self):
        return self.schema.load(
            self.json.loads(self.request.body.decode('utf-8')))

    def chat_id(self):
        return self.data['message']['chat']['id']

    def text(self):
        return self.data['message']['text']
