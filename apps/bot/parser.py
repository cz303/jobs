from bot.serialization import (
    MessageSchema,
    CallbackQuerySchema,
    EditDataCallbackQuery
)
import ujson
from marshmallow.exceptions import ValidationError

__all__ = ['Parser']


class Parser:
    def __init__(self, request):
        self.request = request
        self.message = MessageSchema()
        self.callback_query = CallbackQuerySchema()
        self.edit_date = EditDataCallbackQuery()
        self.json = ujson
        self.data = self.serialization()

    def serialization(self):
        body = self.json.loads(self.request.body.decode('utf-8'))
        try:
            result = self.message.load(body)
        except ValidationError:
            try:
                result = self.callback_query.load(body)
            except ValidationError:
                result = self.edit_date.load(body)
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

    def message_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['message_id']
        else:
            return self.data['message']['message_id']

    def user_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['user']['id']
        else:
            return self.data['message']['user']['id']

    def username(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['user']['username']
        else:
            return self.data['message']['user']['username']
