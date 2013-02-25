from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from bhp_dispatch.forms import DispatchForm
from bhp_dispatch.classes import DispatchController
from bhp_dispatch.exceptions import DispatchAttributeError


@login_required
@csrf_protect
def dispatch(request, dispatch_controller_cls, **kwargs):
    """Receives a list of item identifiers and user selects the producer to dispatch to.

        Args:
            dispatch_controller_cls: a subclass of :class:`DispatchController` coming from a user app, e.g. MochudiDispatchController.
    """
    if not issubclass(dispatch_controller_cls, DispatchController):
        raise AttributeError('Parameter \'dispatch_controller_cls\' must be a subclass of DispatchController.')
    msg = request.GET.get('msg', '')
    producer = request.GET.get('producer', None)
    has_outgoing_transactions = False
    dispatch_url = ''
    dispatch_model_name = ''
    dispatch_admin_url = ''
    if request.method == 'POST':
        form = DispatchForm(request.POST)
        if form.is_valid():
            producer = form.cleaned_data['producer']
            ct = request.POST.get('ct')
            items = request.POST.get('items')
            pks = items.split(',')
            model_cls = ContentType.objects.get(pk=ct).model_class()
            queryset = model_cls.objects.filter(pk__in=pks)
            if producer:
                if not producer.settings_key:
                    raise DispatchAttributeError('Producer attribute settings_key may not be None.')
                for container_instance in queryset:
                    dispatch_controller = dispatch_controller_cls('default', producer.settings_key, container_instance)
                    dispatch_controller.dispatch()
                #already_dispatched, has_outgoing_transactions = dispatch_controller.dispatch_from_view(queryset, **kwargs)
                #if already_dispatched:
                #    msg = 'Selection contains items currently dispatched. Please remove these items and try again.'
                #if has_outgoing_transactions:
                #    msg = 'Producer \'{0}\' has pending outgoing transactions. Sync with server and try again.'.format(producer)
                dispatch_url = dispatch_controller.get_dispatch_url()
                dispatch_model_name = dispatch_controller.get_dispatch_model()._meta.object_name
                dispatch_admin_url = dispatch_controller.get_dispatch_modeladmin_url()
    else:
        ct = request.GET.get('ct')
        items = request.GET.get('items')
        pks = None
        if items:
            pks = items.split(',')
        model_cls = ContentType.objects.get(pk=ct).model_class()
        queryset = model_cls.objects.filter(pk__in=pks)
        form = DispatchForm()

    return render(request, 'dispatch.html', {
        'form': form,
        'ct': ct,
        'items': items,
        'queryset': queryset,
        'producer': producer,
        'msg': msg,
        'has_outgoing_transactions': has_outgoing_transactions,
        'dispatch_url': dispatch_url,
        'dispatch_model_name': dispatch_model_name,
        'dispatch_admin_url': dispatch_admin_url,
        'title': 'Dispatch to Producer',
        })
