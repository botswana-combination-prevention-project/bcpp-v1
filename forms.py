import socket
import re
from django import forms
from bhp_base_form.forms import BaseModelForm
from models import StudySpecific


class StudySpecificForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        device_id = cleaned_data.get('device_id')
        hostname_prefix = cleaned_data.get('hostname_prefix')

        real_hostname = socket.gethostname()
        if not device_id == 0:
            real_device_id = 0
            if re.match(r'[0-9]{2}', real_hostname[len(real_hostname) - 2:]):
                real_device_id = real_hostname[len(real_hostname) - 2:]
            if not str(real_device_id) == str(device_id):
                raise forms.ValidationError("Hostname not equal to \'hostname_prefix\' + \'device_id\'. Got %s<>%s%s" % (real_hostname, hostname_prefix, device_id,))

        if device_id == 0:
            if not real_hostname == hostname_prefix:
                raise forms.ValidationError("Hostname not equal to \'hostname_prefix\' where device_id is '0'. Got %s<>%s" % (real_hostname, hostname_prefix,))

        self.logic.test(cleaned_data, 'machine_type', 'SERVER', 'device_id', 'if_condition_then', 0)

        return super(StudySpecificForm, self).clean()

    class Meta:
        model = StudySpecific
