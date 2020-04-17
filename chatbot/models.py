from peewee import (
    Model,
    SqliteDatabase,
    BooleanField, TextField,
)

db_file = "chatbot.db"

db = SqliteDatabase(db_file)


class NLTKReflections(Model):
    active = BooleanField(default=True)
    reflection_phrase = TextField(null=True)
    reflection = TextField(null=True)

    class Meta:
        database = db
        verbose_name = "Reflection"
        verbose_name_plural = "Reflections"


class NLTKPairs(Model):
    active = BooleanField(default=True)
    question = TextField(null=True)
    answer = TextField(null=True)

    class Meta:
        database = db
        verbose_name = "Question pattern"
        verbose_name_plural = "Question Patterns"


db.connect()

models = [NLTKReflections, NLTKPairs]

for model in models:
    if not db.table_exists(model):
        db.create_tables([model])
