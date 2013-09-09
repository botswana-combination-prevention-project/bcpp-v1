from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from bhp_dispatch.forms import DispatchForm
from bhp_dispatch.classes import DispatchController
from bhp_dispatch.exceptions import DispatchAttributeError


#@login_required
#@csrf_protect
def dispatch(request, dispatch_controller_cls, dispatch_form_cls=None, **kwargs):
    """Receives a list of user container identifiers and user selects the producer to dispatch to.

        Args:
            dispatch_controller_cls: a subclass of :class:`DispatchController` coming from a user app, e.g. MochudiDispatchController.
    """
    if not issubclass(dispatch_controller_cls, DispatchController):
        raise AttributeError('Parameter \'dispatch_controller_cls\' must be a subclass of DispatchController.')
    if not dispatch_form_cls:
        dispatch_form_cls = DispatchForm
    msg = None
    producer = request.GET.get('producer', None)
    has_outgoing_transactions = False
    user_container = ''
    dispatch_url = ''
    user_container_model_name = ''
    user_container_admin_url = ''
    ct = None
    queryset = None
    if request.method == 'POST':
        form = dispatch_form_cls(request.POST)
        if form.is_valid():
            dispatch_url = ''
            producer = form.cleaned_data.get('producer')
            ct = request.POST.get('ct')
            user_container_ct = ct
            survey = form.cleaned_data.get('survey', None)
            items = request.POST.get('items')
            pks = items.split(',')
            user_container_model_cls = ContentType.objects.get(pk=user_container_ct).model_class()
            user_container_model_name = user_container_model_cls._meta.verbose_name
            user_container_admin_url = '/admin/{0}/{1}/'.format(user_container_model_cls._meta.app_label, user_container_model_cls._meta.object_name.lower())
            user_containers = user_container_model_cls.objects.filter(pk__in=pks)
            if producer:
                if not producer.settings_key:
                    raise DispatchAttributeError('Producer attribute settings_key may not be None.')
                for user_container in user_containers:
                    dispatch_controller = dispatch_controller_cls('default', producer.settings_key, user_container, **kwargs)
                    msg = dispatch_controller.dispatch(survey=survey)
                if dispatch_controller:
                    dispatch_url = dispatch_controller.get_dispatch_url()
    else:
        ct = request.GET.get('ct')
        items = request.GET.get('items')
        pks = None
        if items:
            pks = items.split(',')
        model_cls = ContentType.objects.get(pk=ct).model_class()
        queryset = model_cls.objects.filter(pk__in=pks)
        form = dispatch_form_cls()
    messages.add_message(request, messages.INFO, msg)
    return render(request, 'dispatch.html', {
        'form': form,
        'ct': ct,
        'items': items,
        'queryset': queryset,
        'producer': producer,
        'has_outgoing_transactions': has_outgoing_transactions,
        'dispatch_url': dispatch_url,
        'user_container_model_name': user_container_model_name,
        'user_container_admin_url': user_container_admin_url,
        'title': 'Dispatch to Producer',
        })
