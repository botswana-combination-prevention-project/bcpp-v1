from django.db import models
from bhp_basic_models.models import MyBasicModel, MyBasicUuidModel, MyBasicListModel
from bhp_validators.validators import datetime_not_future
from bhp_validators.validators import datetime_not_before_study_start

class Panel(MyBasicModel):
    name = models.CharField("Panel Name", max_length=25)
    comment = models.CharField("Comment", max_length=250, blank=True)

    def __unicode__(self):
        return self.name


class Test(MyBasicModel):
    test_code = models.CharField("Univeral Test ID", max_length=10, unique=True)
    test_name = models.CharField("UTestID Description", max_length=25)
    comment = models.CharField("Comment", max_length=250, blank=True)
    panel = models.ForeignKey(Panel)

    def __unicode__(self):
        return "%s: %s" % (self.test_code,self.test_name)


class AliquotType(MyBasicListModel):
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)

    class Meta:
        ordering = ["short_name"]
        
class AliquotCondition(MyBasicListModel):
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)
    class Meta:
        ordering = ["display_index"]




class Aliquot (MyBasicUuidModel):
    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier', 
        max_length=25, 
        unique=True, 
        help_text="Aliquot identifier", 
        editable=False
        )
    id_int = models.IntegerField(
        editable=False
        )
    id_seed = models.IntegerField(
        editable=False
        )
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
    aliquot_volume = models.DecimalField("Volume in mL / Spots",
        max_digits=10,decimal_places=2
        )
    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        )
    
    def __unicode__(self):
        return self.aliquot_identifier

    #def get_absolute_url(self):
    #    return "/mpepu/labaliquot/%s/" % self.id
        
         
""" 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    
    from bhp_lab.models import ReceiveModel
    class Receive(ReceiveModel):
        subject_consent = models.ForeignKey(SubjectConsent,
        verbose_name="Subject",
        )
"""
    
            
class ReceiveModel (MyBasicUuidModel):
    aliquot = models.OneToOneField(Aliquot)
    datetime_received = models.DateTimeField("Date and time received",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,]
            )
    datetime_drawn = models.DateTimeField("Date and time drawn",
            validators=[
            datetime_not_before_study_start,
            datetime_not_future,]
            )

    def __unicode__(self):
        return unicode(self.lab_aliquot)

    #def get_absolute_url(self):
    #    return "//labreceive/%s/" % self.id
    class Meta:
        abstract=True

class Order(MyBasicUuidModel):
    aliquot = models.ForeignKey(Aliquot)    

class Result(MyBasicUuidModel):
    order = models.ForeignKey(Order)

class ResultItem(MyBasicUuidModel):
    result = models.ForeignKey(Result)
    


