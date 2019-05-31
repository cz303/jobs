from marshmallow import (
    Schema,
    fields
)


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


class MessageSchema(Schema):
    message = fields.Nested(Message)
    update_id = fields.Integer()
