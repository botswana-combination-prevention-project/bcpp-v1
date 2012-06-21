""" MySQL composite indexing. Also kinda works with SQLite3.

Looks for a _index_together tuple of column-name-tuples in the model class
Creates non-unique composite index based on that

Important : That tuple must be in the model, not the Meta class!
It's not a very Django-ish way of doing things, but I wasn't really willing
to hacking around in Django's Meta options. Meta ... it sounds so ... Ruby.

Usage is like so ...

class MyModel(models.Model):
    field_1 = models.IntegerField()
    field_2 = models.IntegerField()
    
    field_3 = models.IntegerField()
    field_4 = models.IntegerField()
    
    _index_together = (('field_1', 'field_2'), ('field3', 'field4'))

"""

from django.db import connection
from django.conf import settings

def create_index(model):
    meta = getattr(model, '_meta', None)
    if not meta: return 0
    
    #if settings.DATABASE_ENGINE == 'mysql':
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':    
        func = create_index_mysql
    #elif settings.DATABASE_ENGINE == 'sqlite3':
    #    func = create_index_sqlite3
    else:
        return 0
    
    successes = 0
    
    index_tuples = getattr(model, '_index_together', [])
    for index_tuple in index_tuples:
        columns = [meta.get_field(field).column for field in index_tuple]
        name = '_'.join(columns)[:63]
        table = meta.db_table
        successes += func(name, table, columns)
        
    if successes:
        print '%d indices created' % successes
    return successes

def create_index_mysql(name, table, columns):
    cursor = connection.cursor()    
    sql = "CREATE INDEX %s ON %s (%s)" % (
        name, table, ', '.join(columns))
        
    from MySQLdb import OperationalError
    try:
        cursor.execute(sql)
        return 1
    except OperationalError as x:
        if x.args[0] != 1061: # 1061 means duplicate key name / we can ignore
            raise
        return 0
    finally:
        cursor.close()


def create_index_sqlite3(name, table, columns):
    cursor = connection.cursor()
    sql = "CREATE INDEX IF NOT EXISTS %s ON %s (%s)" % (
        name, table, ', '.join(columns))
    try:
        cursor.execute(sql)
        return 1
    finally:
        cursor.close()


def create_all_indices(sender, *args, **kwds):
    from django.db import models
    model_list = models.get_models(sender)
    for model in model_list:
        create_index(model)


from django.db.models import signals
signals.post_syncdb.connect(create_all_indices)
