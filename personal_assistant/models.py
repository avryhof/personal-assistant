import peewee

db_file = "chatbot.db"

db = peewee.SqliteDatabase(db_file)


class Device(peewee.Model):
    name = peewee.CharField(max_length=100, null=True)
    ip_address = peewee.CharField(max_length=30, null=True)
    port = peewee.IntegerField(null=True)
    service = peewee.CharField(max_length=100, null=True)
    description_url = peewee.TextField(null=True)


class NLTKReflections(peewee.Model):
    active = peewee.BooleanField(default=True)
    reflection_phrase = peewee.TextField(null=True)
    reflection = peewee.TextField(null=True)

    class Meta:
        database = db
        verbose_name = "Reflection"
        verbose_name_plural = "Reflections"


class NLTKPairs(peewee.Model):
    active = peewee.BooleanField(default=True)
    question = peewee.TextField(null=True)
    answer = peewee.TextField(null=True)

    class Meta:
        database = db
        verbose_name = "Question pattern"
        verbose_name_plural = "Question Patterns"


db.connect()

models = [Device, NLTKReflections, NLTKPairs]

for model in models:
    if not db.table_exists(model):
        db.create_tables([model])
