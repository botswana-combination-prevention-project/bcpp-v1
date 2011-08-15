from django.db.models import CharField, DateField, DateTimeField, DecimalField, IntegerField

def describe_data(self, model):

    model = model
    opts = model._meta

    # basic summary
    q={}
    summary = {}
    for field in opts.fields:
        if isinstance(field, (DateTimeField, DateField)):
            q=model.objects.all().aggregate(Count(field.name), Max(field.name), Min(field.name))
        elif isinstance(field, (IntegerField, DecimalField)):
            q=model.objects.all().aggregate(Count(field.name), Avg(field.name), Max(field.name), Min(field.name), StdDev(field.name), Variance(field.name))    
        elif isinstance(field, (CharField)):
            q=model.objects.all().aggregate(Count(field.name))    
        else:
            q={}
        summary[field.name] = q


    q={}
    group={}
    # basic grouping on char fields    
    for field in opts.fields:
        if isinstance(field, (CharField)):
            #group on choices tuple
            if field.choices:
                for choice in field.choices:
                    q=model.objects.values(field.name).annotate(count=Count(field.name))
                    group[field.name] = q        
            #group on foreignkey
            elif isinstance(field, models.ForeignKey):
                for fld in field.related.parent_model._meta.fields:
                    if fld.name == 'name':
                        fld_string = '%s__%s__name' % (fld.name, fld.related.parent_model._meta.module_name)
                        q=model.objects.values(fld_string).annotate(count=Count(fld_string))
                        raise TypeError(q)
                        group[field.name] = q
                        

    print summary
    
    print group
