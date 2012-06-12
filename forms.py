from django import forms
from bhp_base_form.classes import BaseModelForm
from lab_requisition.forms import BaseRequisitionForm
#from lab_packing.models import PackingList

"""
The "requisition" model is required for the code
in the clean() method below. 

In the local xxxx_lab app add something this to forms

from lab_packing.forms import PackingListForm

class PackingListForm (BasePackingListForm): 

    def clean(self):
        self.requisition  = [InfantRequisition,] 
        return  super(PackingListForm, self).clean()


    class Meta:
        model = PackingList 

"""        


class BasePackingListForm(BaseRequisitionForm):

    requisition = None
    
    def clean(self):
    
        cleaned_data = self.cleaned_data 
        
        if not self.requisition:
            raise forms.ValidationError('Class attribute requisition cannot be None. Was it not defined in the local \'..._lab\' forms.py app?')  
        if not isinstance(self.requisition, list):
            self.requisition = [self.requisition,]
        for specimen_identifier in cleaned_data.get('list_items').replace('\r', '').split('\n'):
            if specimen_identifier:
                found = False
                for requisition in self.requisition:
                    if requisition.objects.filter(specimen_identifier=specimen_identifier):
                        found = True
                        break
                if not found:   
                    raise forms.ValidationError('%s specimen identifier \'%s\' not found' % (requisition._meta.verbose_name, specimen_identifier,))

        return cleaned_data
  
        
# PackingList
class BasePackingListItemForm (BaseModelForm): 

    def clean(self):
   
        return  super(BasePackingListItemForm, self).clean()
       
