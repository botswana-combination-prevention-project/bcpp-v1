from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from bhp_sync.models import Transaction

@login_required
def tx_to_response(request, **kwargs):
    transactions = Transaction.objects.filter(is_sent=False).order_by('timestamp')
    tx = []
    for transaction in transactions:
        tx.append(transaction.tx)
    return HttpResponse(tx, mimetype = 'application/json')

