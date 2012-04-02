from datetime import date, datetime, timedelta
from django import forms
from lab_requisition.forms import BaseRequisitionForm
from lab_packing.models import PackingList

"""
The "requisition" model is required for the code
in the clean() method below. 

In the local xxxx_lab app add something this to forms

from lab_packing.forms import PackingListForm

class InfantPackingListForm (PackingListForm): 

    def clean(self):
        self.requisition  = InfantRequisition 
        return  super(InfantPackingListForm, self).clean()


    class Meta:
        model = InfantPackingList 

"""        


class PackingListForm(BaseRequisitionForm):

    requisition = None
    
    def clean(self):
    
        cleaned_data = self.cleaned_data 
        
        if not self.requisition:
            raise forms.ValidationError('Packing lists may not be saved via the \'lab_packing\' app. Requisition is unknown. Go to your local _lab app.')  
        if not isinstance(self.requisition, list):
            self.requisition = [self.requisition,]
        list_items = cleaned_data.get('list_items')
        lst = list_items.replace('\r', '').split('\n')
        for item in lst:
            if item:
                found = False
                for requisition in self.requisition:
                    if requisition.objects.filter(specimen_identifier=item):
                        found = True
                        break
                if not found:   
                    raise forms.ValidationError('%s for packing list item \'%s\' not found' % (requisition._meta.verbose_name, item,))

        return cleaned_data

    class Meta:
        model = PackingList  
