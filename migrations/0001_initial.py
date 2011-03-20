# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        try:
            # Deleting model 'RegisteredSubjectAppointment'
            db.delete_table('bhp_appointment_registeredsubjectappointment')
        except:
            pass



    def backwards(self, orm):
        pass


    models = {
        
    }

    complete_apps = ['bhp_appointment']
