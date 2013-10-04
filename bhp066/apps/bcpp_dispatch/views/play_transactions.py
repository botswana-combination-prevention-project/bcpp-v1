import socket
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from ..classes import BcppConsumer
from bhp066.settings.email_settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


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
    if not (EMAIL_HOST or EMAIL_PORT or EMAIL_HOST_USER or EMAIL_HOST_PASSWORD):
        raise ImproperlyConfigured("Ensure that EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD are set in the email_settings file")
    send_mail('Consuming status of BCPP incoming transactions;-'+str(socket.gethostname()),message, EMAIL_HOST_USER+'@bhp.org.bw',['django@bhp.org.bw'], fail_silently=False)
    
    return redirect('/dispatch/bcpp/sync/')
#     return render_to_response('household_return.html', {
#                                'queryset': all_containers,
#                                'producer': ref_container.producer.name
#                                },
#                               context_instance=RequestContext(request)
#                             )