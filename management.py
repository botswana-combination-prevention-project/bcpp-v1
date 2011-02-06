from django.dispatch import dispatcher
from django.db.models import signals
 
def my_syncdb_func():
    # put your code here...
    
dispatcher.connect(my_syncdb_func, signal=signals.post_syncdb)

