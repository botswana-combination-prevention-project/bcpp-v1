from datetime import datetime

from model_label import ModelLabel


class QuerysetLabel(ModelLabel):
    """ Print a label building the template and context from the model."""
    def __init__(self, *args, **kwargs):
        self.default_template_name = 'default_queryset_label'
        self.default_template_string = ('^XA\n'
                '^FO325,5^A0N,15,20^FD${item_count}/${item_count_total}^FS\n'
                '^FO320,20^BY1,3.0^BCN,50,N,N,N\n'
                '^BY^FD${barcode_value}^FS\n'
                '^FO320,80^A0N,15,20^FD${barcode_value}^FS\n'
                '^FO325,100^A0N,15,20^FD${panel} ${aliquot_type}^FS\n'
                '^FO325,152^A0N,20^FD${user_created}^FS\n'
                '^FO325,152^A0N,20^FD${created}^FS\n'
                '^XZ')
        super(QuerysetLabel, self).__init__(*args, **kwargs)

    def print_label(self, request, queryset):
        for instance in queryset:
            self.prepare_label_context(instance=instance)
            super(QuerysetLabel, self).print_label(request, request.META.get('REMOTE_ADDR'))

    def prepare_label_context(self, **kwargs):
        """ Add all the model fields for instance to the label context.

        Users may override this to set a custom label context
        that matches the template."""
        context = {}
        instance = kwargs.get('instance')
        for field in instance._meta.fields:
            if isinstance(getattr(instance, field.attname, field.attname), datetime):
                timestamp = getattr(instance, field.attname, field.attname).strftime('%Y-%m-%d %H:%M')
                context.update({field.attname: timestamp})
            else:
                context.update({field.attname: getattr(instance, field.attname, field.attname)})
        context.update({'barcode_value': instance.barcode_value()})
        self.is_prepared = True
        self.label_context = context
        return self.label_context
