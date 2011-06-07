from django import forms

class MyModelForm(forms.ModelForm):

    def clean(self):
    
        cleaned_data = self.cleaned_data 

        other =[]
        [other.append(k) for k in cleaned_data.iterkeys() if cleaned_data[k] == 'OTHER']
        for k in other:
            if k+'_other' in cleaned_data:
                if not cleaned_data[k+'_other']:        
                    raise forms.ValidationError("If %s is 'OTHER', please specify. You wrote '%s'" %  (k,cleaned_data[k+'_other']))

        super(MyModelForm, self).clean()
    
        return cleaned_data

