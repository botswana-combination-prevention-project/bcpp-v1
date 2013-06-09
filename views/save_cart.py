import itertools
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.db.models import get_model


def save_cart(request):
    """Dispatch households in shopping cart to netbook.
    """
    #Make sure we have identifiers in our session
    Household = get_model('mochudi_household', 'household')
    item_model_cls = Household
    item_identifier_field = 'household_identifier'

    if 'identifiers' in request.session:
        if len(request.session['identifiers']) > 0:
            identifiers = request.session['identifiers']
            # TODO: code to send identifies to be dispatched
#            pks = item_model_cls.objects.filter(**{'{0}__in'.format(item_identifier_field): identifiers}).values_list('pk')
            pks = item_model_cls.objects.filter(household_identifier__in=identifiers).values_list('pk')
            selected = list(itertools.chain(*pks))
            content_type = ContentType.objects.get_for_model(Household)
            return HttpResponseRedirect("/dispatch/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))

            try:
                del request.session['identifiers']
                del request.session['icon']
            except KeyError:
                pass
