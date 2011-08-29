from datetime import *
from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from bhp_lab_order.models import Order

class AliquotAutocomplete(AutocompleteSettings):

    search_fields = ('^aliquot_identifier',)
autocomplete.register(Order.aliquot, AliquotAutocomplete)

class OrderAutocomplete(AutocompleteSettings):
    search_fields = ('^order_identifier',)

#autocomplete.register(Order.aliquot, AliquotAutocomplete)


class OrderAdmin(AutocompleteAdmin,MyModelAdmin):

    def save_model(self, request, obj, form, change):
    
        if not change:
            obj.order_identifier = self.model.objects.get_identifier() 

        if change:
            obj.user_modified=request.user
            
    
        save = super(OrderAdmin, self).save_model(request, obj, form, change)
        return save


    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj = None):
        if obj: #In edit mode
            return ('aliquot','order_identifier',) + self.readonly_fields
        else:
            return self.readonly_fields  
    
    fields = ('order_datetime', 'panel', 'aliquot', 'comment', 'dmis_reference', )
    
    list_display = ('order_identifier', 'order_datetime', 'panel', 'aliquot', 'dmis_reference')
    
admin.site.register(Order, OrderAdmin)

