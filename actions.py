import csv
import datetime
from django.http import HttpResponse
try:
    from django.db.models.constants import LOOKUP_SEP
except:
    # django 1.5
    from django.db.models.sql.constants import LOOKUP_SEP
from django.db.models import ManyToManyField


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, extra_fields=None, header=True):
    """
    Return an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    
    ...in my_app/admin.py add this import:
    from bhp_common.actions import export_as_csv_action
    
    ...and this to your modeladmin class:        
    actions = [export_as_csv_action("CSV Export", 
        fields=[], 
        exclude=[],
        extra_fields=[],
        )]
    
    use extra_fields to access field attributes from related models. Pass a 
    list of dictionaries [{'label': 'query_string'}, {}, ...]
    
    """
    def my_getattr(obj, query_list):

        """ Recurse on result of getattr() with a given query string as a list.

                The query_list is based on a django-style query string 
                split on '__' into a list.
                For example 'field_attr__model_name__field_attr' split to 
                ['field_attr', 'model_name', 'field_attr']
        """

        if len(query_list) > 1:
            try:
                return my_getattr(getattr(obj, query_list[0]), query_list[1:])
            except:
                # DoesNotExist
                return '(none)'
        return getattr(obj, query_list[0])

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/

        Added exra_fields and changed accordingly
        """

        #export_queryset_as_csv(modeladmin, request, queryset)

        opts = modeladmin.model._meta

        field_names = [field.name for field in opts.fields]

        # add extra fields to field_names, these are django-style query_strings  
        if extra_fields:
            # extra fields is list of dicts of [{'label': 'query_string'}, {}...]
            for item in extra_fields:
                field_names.extend(item.values())

        field_names = set(field_names)

        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')

        response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (unicode(opts).replace('.', '_'), datetime.datetime.now().strftime('%Y%m%d'))

        writer = csv.writer(response)

        if header:
            header_row = list(field_names)
            if extra_fields:
                for item in extra_fields:
                    if item.values()[0] in header_row:
                        header_row[header_row.index(item.values()[0])] = item.keys()[0]
        # queryset comes from action call. loop over queryset objects
        header_complete = False
        for obj in queryset:
            # start a new row as a list
            if not header_complete:
                for m2m in obj._meta.many_to_many:
                    header_row.append(m2m.name)
                writer.writerow(header_row)
                header_complete = True
            row = []
            for field in field_names:
                if field in queryset.model.__dict__:
                    # is a field_attr for the queryset.model, append field object value to row
                    row.append(unicode(getattr(obj, field)).encode("utf-8", "replace"))
                else:
                    # is not a field attribute for this model, must be a django-style query_string
                    # split on LOOKUP_SEP
                    query_list = field.split(LOOKUP_SEP)
                    # recurse to last field object to get value
                    item = my_getattr(obj, query_list)
                    # append to row
                    row.append(unicode(item).encode("utf-8", "replace"))
            for m2m in obj._meta.many_to_many:
                values = '; '.join([item.name.encode("utf-8", "replace") for item in getattr(obj, m2m.name).all()])
                row.append(values)
            writer.writerow(row)

            #writer.writerow([unicode(getattr(obj, field)).encode("utf-8","replace") for field in field_names])
            #writer.writerow([unicode(obj[field]).encode("utf-8","replace") for field in field_names])            

        return response

    export_as_csv.short_description = description

    return export_as_csv
