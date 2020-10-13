from peewee import *

import datetime

DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    entry_id = IntegerField(primary_key=True, unique=True)
    title = CharField(max_length=255, default="Untitled")
    date = DateTimeField(default=datetime.datetime.now)
    timespent = IntegerField()
    post = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp')

    @classmethod
    def create_entry(cls, title, post):
        cls.create(title=title, post=post)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
