import mongoengine as me


class Cat(me.Document):
    id = me.StringField(primary_key=True)
    name = me.StringField(max_length=200, required=True)
    color = me.StringField(required=True)
    foods = me.ListField(child=me.StringField(required=False), required=False)
    sex = me.StringField(required=False)
