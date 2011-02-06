from datetime import date, datetime, timedelta
from django import forms
from django.contrib.admin import widgets                                       

class MyAf002Form(forms.ModelForm):
    
    class Meta:
        model = VisitTracking        

    def clean(self):

        cleaned_data = self.cleaned_data
    
        """
        check subjectconsent initials with householdstructuremember initials
        """
        my_initials = cleaned_data.get("initials")
        my_household_structure_member = cleaned_data.get("household_structure_member")
        if my_initials and my_household_structure_member:
            # Only do something if both fields are valid so far.
            if my_household_structure_member.initials != my_initials:
                raise forms.ValidationError("Initials do not match. The initials recorded in the household member's information are '%s' but you wrote '%s'" % (my_household_structure_member.initials,my_initials))
            
        """
        check first name matches householdstructuremember
        """
        my_first_name = cleaned_data.get("first_name")
        if my_first_name and my_household_structure_member:
            if my_household_structure_member.first_name != my_first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (my_household_structure_member.first_name,my_first_name))
        
        """
        check subjectconsent gender with householdstructuremember gender
        """
        my_gender = cleaned_data.get("gender")
        if my_gender and my_household_structure_member:
            if my_household_structure_member.gender != my_gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (my_household_structure_member.gender, my_gender))

        """
        check age now
        """
        this_dob = cleaned_data.get("dob")
        if this_dob and my_household_structure_member and this_dob != date.today():
            this_age = (date.today() - this_dob)
            age = my_household_structure_member.age_in_years
            if this_age.days/365 != age:
                raise forms.ValidationError("Date of birth does not match. Age in the \
                        household member's information is '%s' but you wrote '%s' \
                        which is '%s'." % (age,this_dob, this_age.days/365))

        # Always return the full collection of cleaned data.
        return cleaned_data
