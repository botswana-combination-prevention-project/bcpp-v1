from django.db import models
from django.db.models.query import QuerySet
from mochudi_survey.models import Survey

class StudySpecificManager(models.Manager):

    def get_query_set(self):
   
        qs  = QuerySet(self.model, using=self._db).all()
        if not qs:
            raise ValueError, 'Appplication is accessing model StudySpecific but you have not populated it. Please do so before continuing.'
            
        qs  = QuerySet(self.model, using=self._db).filter(pk=qs[0].pk)                    
        
        return qs

