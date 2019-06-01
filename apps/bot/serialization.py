from marshmallow import (
    Schema,
    fields
)

__all__ = [
    'CallbackQuerySchema',
    'MessageSchema'
]


class User(Schema):
    first_name = fields.String()
    id = fields.Integer()
    is_bot = fields.Boolean()
    language_code = fields.String()
    username = fields.String()


class Chat(Schema):
    first_name = fields.String()
    id = fields.Integer()
    type = fields.String()
    username = fields.String()


class Message(Schema):
    chat = fields.Nested(Chat)
    date = fields.Integer()
    entities = fields.List(fields.Dict())
    user = fields.Nested(User, data_key='from')
    message_id = fields.Integer()
    text = fields.String()


class InlineMessage(Message):
    reply_markup = fields.List(fields.List(fields.Dict()))


class MessageSchema(Schema):
    message = fields.Nested(Message)
    update_id = fields.Integer()


class CallbackQuery(Schema):
    id = fields.String()
    user = fields.Nested(User, data_key='from')
    message = fields.Nested(InlineMessage)
    chat_instance = fields.String()
    data = fields.String()


class CallbackQuerySchema(Schema):
    update_id = fields.Integer()
    callback_query = fields.Nested(CallbackQuery)
