from marshmallow import Schema, fields


class IsAliveSchema(Schema):
    alive = fields.Bool(True)
