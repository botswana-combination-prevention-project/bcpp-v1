import itertools
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from bhp_map.classes import mapper
from bhp_map.exceptions import MapperError


def save_cart(request):
    """Dispatch households in shopping cart to netbook.
    """
    #Make sure we have identifiers in our session
    mapper_name = request.GET.get('mapper_name', '')
    if not mapper.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = mapper.get_registry(mapper_name)
        if 'identifiers' in request.session:
            if len(request.session['identifiers']) > 0:
                identifiers = request.session['identifiers']
                # TODO: code to send identifies to be dispatched
                pks = m.item_model_cls().objects.filter(**{'{0}__in'.format(m.identifier_field_attr): identifiers}).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(m.item_model_cls())
                return HttpResponseRedirect("/dispatch/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
                try:
                    del request.session['identifiers']
                    del request.session['icon']
                except KeyError:
                    pass
