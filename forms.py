from datetime import date, datetime, timedelta
from django import forms
from django.db.models import Avg, Max, Min, Count
from django.contrib.admin import widgets   
from bhp_visit.models import Appointment                                    

class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment        

    def clean(self):

        cleaned_data = self.cleaned_data  

        appt_datetime = cleaned_data.get("appt_datetime")
        appt_status = cleaned_data.get("appt_status")
        registered_subject = cleaned_data.get("registered_subject")
        visit_definition = cleaned_data.get("visit_definition") 
        visit_instance =  cleaned_data.get("visit_instance") 

        # check appointment date relative to status    
        # postive t1.days => is a future date [t1.days > 0]
        # negative t1.days => is a past date [t1.days < 0]
        # zero t1.days => now (regardless of time) [t1.days == 0]
        t1 = appt_datetime.date() - date.today()
        if appt_status == 'cancelled':
            pass
        elif appt_status == 'done':
            # must not be future
            if t1.days > 0:
                raise forms.ValidationError("Appointment is 'done'. Date cannot be a future date. You wrote '%s'" % appt_datetime)
            # cannot be done if no visit report, but how do i get to the visit report??
                
        elif appt_status == 'new':
            # must be future
            if t1.days < 0:            
                raise forms.ValidationError("Appointment is 'new', the appointment date must be a future date. You wrote '%s'" % appt_datetime)             
                
            # for new appointments, no matter what, appt_datetime must be greater than 
            # any existing appointment for this subject and visit code
            aggr = Appointment.objects.filter(
                registered_subject = registered_subject, 
                visit_definition__code = visit_definition.code).aggregate(Max('appt_datetime'))
            if aggr['appt_datetime__max'] <> None:
                t1 = aggr['appt_datetime__max'] - appt_datetime
                if t1.days >= 0:
                    raise forms.ValidationError("An appointment with appointment date greater than or equal to this date already exists'. You wrote '%s'" % appt_datetime)
    
        elif appt_status == 'in_progress':
            # check if any other appointments in progress for this registered_subject
            if Appointment.objects.filter(registered_subject = registered_subject, appt_status = 'in_progress').exclude(visit_definition__code = visit_definition.code, visit_instance = visit_instance):
                appointments = Appointment.objects.filter(registered_subject = registered_subject, appt_status = 'in_progress').exclude(visit_definition__code = visit_definition.code, visit_instance = visit_instance)
                raise forms.ValidationError("Another appointment is 'in progress'. Update appointment %s.%s before changing this scheduled appointment to 'in progress'" % (appointments[0].visit_definition.code, appointments[0].visit_instance))
        else:
            raise TypeError("Unknown appt_status passed to clean method in form AppointmentForm. Got %s" % appt_status)
            #must be future

        # Always return the full collection of cleaned data.
        return cleaned_data
"""
class BaseVisitTrackingForm(forms.ModelForm):
    
    class Meta:
        model = VisitTracking        

    def clean(self):

        cleaned_data = self.cleaned_data
    
       
        #check subjectconsent initials with householdstructuremember initials
        my_initials = cleaned_data.get("initials")
        my_household_structure_member = cleaned_data.get("household_structure_member")
        if my_initials and my_household_structure_member:
            # Only do something if both fields are valid so far.
            if my_household_structure_member.initials != my_initials:
                raise forms.ValidationError("Initials do not match. The initials recorded in the household member's information are '%s' but you wrote '%s'" % (my_household_structure_member.initials,my_initials))
            
        
        #check first name matches householdstructuremember
        my_first_name = cleaned_data.get("first_name")
        if my_first_name and my_household_structure_member:
            if my_household_structure_member.first_name != my_first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (my_household_structure_member.first_name,my_first_name))
      
        #check subjectconsent gender with householdstructuremember gender
        my_gender = cleaned_data.get("gender")
        if my_gender and my_household_structure_member:
            if my_household_structure_member.gender != my_gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (my_household_structure_member.gender, my_gender))

     
        #check age now
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
"""
        

