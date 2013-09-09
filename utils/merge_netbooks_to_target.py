from django.core import serializers
from django.db.utils import IntegrityError
from bhp_merge.utils import MergeSourceWithTarget
from bhp_netbook.models import Netbook 

"""
to call from python manage.py shell_plus

from bhp_merge.utils import merge_netbooks_to_target
merge_netbooks_to_target()
"""

def merge_netbooks_to_target(**kwargs):
    """
    for each netbook listed in model Netbook, run MergeSourceWithTarget
    """
    # pass these k/v to
    # ... bypass the exception trap and allow mysql to fail with its error
    show_error=kwargs.get("show_error", False)
    # .. limit to the db of only this netbook
    netbook=kwargs.get("netbook")            
    if netbook:
        netbooks = Netbook.objects.filter(name__exact=netbook)        
    else:
        netbooks = Netbook.objects.all()
    #for each netbook run the merge    
    for nbk in netbooks:
        # each netbook has a named db. in most cases the hostname of the netbook is
        # the same as the restored db name
        netbook_db = nbk.db_name
        # merge the netbook db (source) with the target db. 
        MergeSourceWithTarget(
            app_label_name='mochudi',
            import_category='data',
            target_database='mpp',
            source_database=netbook_db,
            show_error=show_error,
            )
