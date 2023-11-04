import mongoengine as me
import datetime


class House(me.Document):
    meta = {"collection": "houses"}
    name = me.StringField(required=True)
    width = me.FloatField(required=True)
    height = me.FloatField(required=True)
    volume = me.FloatField(required=True)
    created_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )
    updated_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )
