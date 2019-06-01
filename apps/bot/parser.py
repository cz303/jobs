from bot.serialization import (
    MessageSchema,
    CallbackQuerySchema
)
import ujson
from marshmallow.exceptions import ValidationError

__all__ = ['Parser']


class Parser:
    def __init__(self, request):
        self.request = request
        self.message = MessageSchema()
        self.callback_query = CallbackQuerySchema()
        self.json = ujson
        self.data = self.serialization()

    def serialization(self):
        body = self.json.loads(self.request.body.decode('utf-8'))
        try:
            result = self.message.load(body)
        except ValidationError:
            result = self.callback_query.load(body)
        return result

    def chat_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['chat']['id']
        else:
            return self.data['message']['chat']['id']

    def text(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['data']
        else:
            return self.data['message']['text']
