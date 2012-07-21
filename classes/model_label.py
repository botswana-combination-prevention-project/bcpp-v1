from datetime import datetime

from django.contrib import messages

from lab_barcode.models import ZplTemplate
from label import Label


class ModelLabel(Label):
    """ Print a label building the template and context from the model."""

    def print_label_on_save_model(self, request, instance):
        self.prepare_label_context(instance=instance)
        template = self.get_template(instance)
        msg, success = self.print_label(template, request.META.get('REMOTE_ADDR'))
        if not success:
            messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.SUCCESS,
                                 '{0} for \'{1}\''.format(msg, instance.barcode_value()))

    def prepare_label_context(self, **kwargs):
        """ Add all the model fields to the template context"""
        instance = kwargs.get('instance')
        for field in instance._meta.fields:
            if isinstance(getattr(instance, field.attname, field.attname), datetime):
                timestamp = getattr(instance, field.attname, field.attname).strftime('%Y-%m-%d %H:%M')
                self.label_context.update({field.attname: timestamp})
            else:
                self.label_context.update({field.attname: getattr(instance, field.attname, field.attname)})
        self.label_context.update({'barcode_value': instance.barcode_value()})
        self.is_prepared = True
        return self.label_context

    def get_template(self, instance):
        try:
            label_template = instance.label_template()
        except:
            label_template = 'default_model_label'
        try:
            template = ZplTemplate.objects.get(name=label_template)
        except:
            template = ZplTemplate()
            template.name = label_template
            template.template = ('^XA\n'
                '^FO325,5^A0N,15,20^FD${item_count}/${item_count_total}^FS\n'
                '^FO320,20^BY1,3.0^BCN,50,N,N,N\n'
                '^BY^FD${barcode_value}^FS\n'
                '^FO320,80^A0N,15,20^FD${barcode_value}^FS\n'
                '^FO325,100^A0N,15,20^FD${panel} ${aliquot_type}^FS\n'
                '^FO325,152^A0N,20^FD${user_created}^FS\n'
                '^FO325,152^A0N,20^FD${created}^FS\n'
                '^XZ')

            """^XA
                ^FO325,15^A0N,15,20^FDBHHRL^FS
                '^FO310,30^BY2,3^BCN,75,N,N,N\n'
                ^BY^FD${barcode_value}^FS
                ^FO320,110^A0N,15,20^FD${barcode_value}^FS
                ^FO325,130^A0N,15,20^FDCD4^FS
                ^FO325,150^A0N,20^FD${created}^FS
                ^XZ"""
        return template
