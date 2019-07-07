from marshmallow import (
    Schema,
    fields
)

__all__ = (
    'CallbackQuerySchema',
    'MessageSchema',
    'EditDataCallbackQuery',
    'Search',
    'Inline',
    'Contact',
)


class User(Schema):
    first_name = fields.String()
    id = fields.Integer()
    is_bot = fields.Boolean()
    language_code = fields.String()
    username = fields.String()


class Chat(Schema):
    first_name = fields.String()
    last_name = fields.Str()
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


class ReplyMarkup(Schema):
    inline_keyboard = fields.List(fields.List(fields.Dict()))


class InlineMessage(Message):
    reply_markup = fields.Nested(ReplyMarkup)


class ContactObj(Schema):
    phone_number = fields.Str()
    first_name = fields.Str()
    user_id = fields.Integer()


class ContactMessage(Message):
    contact = fields.Nested(ContactObj)
    reply_to_message = fields.Nested(Message)


class InlineMessageEditDate(Message):
    reply_markup = fields.Nested(ReplyMarkup)
    edit_date = fields.Integer()


class MessageSchema(Schema):
    message = fields.Nested(Message)
    update_id = fields.Integer()


class CallbackQueryEditDate(Schema):
    id = fields.String()
    user = fields.Nested(User, data_key='from')
    message = fields.Nested(InlineMessageEditDate)
    chat_instance = fields.String()
    data = fields.String()


class CallbackQuery(CallbackQueryEditDate):
    message = fields.Nested(InlineMessage)
    chat = fields.Nested(Chat)
    date = fields.Integer()
    text = fields.String()
    entities = fields.List(fields.Dict())
    reply_markup = fields.Nested(ReplyMarkup)


class CallbackQuerySchema(Schema):
    update_id = fields.Integer()
    callback_query = fields.Nested(CallbackQuery)


class EditDataCallbackQuery(Schema):
    update_id = fields.Integer()
    callback_query = fields.Nested(CallbackQueryEditDate)


class InlineQuery(Schema):
    id = fields.Str()
    user = fields.Nested(User, data_key='from')
    query = fields.Str()
    offset = fields.Str()


class Search(Schema):
    update_id = fields.Integer()
    inline_query = fields.Nested(InlineQuery)


class Inline(Schema):
    update_id = fields.Integer()
    message = fields.Nested(InlineMessage)


class Contact(Schema):
    update_id = fields.Integer()
    message = fields.Nested(ContactMessage)
