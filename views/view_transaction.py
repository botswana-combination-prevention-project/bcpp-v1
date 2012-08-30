from django.shortcuts import render_to_response
from django.db.models import get_model
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import TextField
from bhp_crypto.fields import EncryptedTextField


@login_required
def view_transaction(request, **kwargs):
    model_name = kwargs.get('model_name')
    pk = kwargs.get('pk')
    model = get_model('bhp_sync', model_name)
    model_instance = model.objects.get(pk=pk)
    textfields = {}
    charfields = {}
    for field in model_instance._meta.fields:
        if isinstance(field, (TextField, EncryptedTextField)):
            textfields.update({field.name: getattr(model_instance, field.name)})
        else:
            charfields.update({field.name: getattr(model_instance, field.name)})
    return render_to_response('transaction.html',
        {'charfields': charfields, 'textfields': textfields},
        context_instance=RequestContext(request))
