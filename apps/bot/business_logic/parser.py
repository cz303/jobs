from bot.models.serialization import (
    MessageSchema,
    CallbackQuerySchema,
    EditDataCallbackQuery,
    Search,
    Inline,
    Contact,
)
import ujson
from marshmallow.exceptions import ValidationError

__all__ = ('Parser',)


class Parser:
    def __init__(self, request):
        self.request = request
        self.message = MessageSchema()
        self.callback_query = CallbackQuerySchema()
        self.edit_date = EditDataCallbackQuery()
        self.search = Search()
        self.inline = Inline()
        self.contact = Contact()
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
                try:
                    result = self.edit_date.load(body)
                except ValidationError:
                    try:
                        result = self.search.load(body)
                    except ValidationError:
                        try:
                            result = self.inline.load(body)
                        except ValidationError:
                            result = self.contact.load(body)
        return result

    def chat_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['chat']['id']
        elif 'inline_query' in self.data:
            return self.data['inline_query']['id']
        else:
            return self.data['message']['chat']['id']

    def text(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['data']
        elif 'inline_query' in self.data:
            return self.data['inline_query']['query']
        elif 'contact' in self.data['message']:
            return self.data['message']['contact']
        else:
            return self.data['message']['text']

    def message_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['message_id']
        elif 'inline_query' in self.data:
            return self.data['inline_query']['id']
        else:
            return self.data['message']['message_id']

    def callback_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['id']

    def user_id(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['user']['id']
        elif 'inline_query' in self.data:
            return self.data['inline_query']['user']['id']
        else:
            return self.data['message']['user']['id']

    def username(self):
        if 'callback_query' in self.data:
            return self.data['callback_query']['message']['user']['username']
        elif 'inline_query' in self.data:
            return self.data['inline_query']['user']['username']
        else:
            try:
                return self.data['message']['user']['username']
            except KeyError as error:
                print(str(error))
