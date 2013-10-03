from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from ..classes import BcppConsumer


@login_required
def play_transactions(request, **kwargs):
    """ Play all the incoming transactions pending on the server
    """
    consumer = BcppConsumer()
    try:
        consumer.consume()
    except:
        pass
    message = consumer.get_consume_feedback()
    messages.add_message(request, messages.INFO, message)
    
    return redirect('/dispatch/bcpp/sync/')
#     return render_to_response('household_return.html', {
#                                'queryset': all_containers,
#                                'producer': ref_container.producer.name
#                                },
#                               context_instance=RequestContext(request)
#                             )