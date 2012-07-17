Building Model Rules
====================

The order in which the classes are listed matters. If rules refer to the same
model, only the result of the last rule will matter. In the example below, 
the target_model 'hivhistorycd4' is referred to in HivHistoryBucket and ObHistoryBucket.
Since ObHistoryBucket rules will run last, the result of the HivHistoryBucket
rule referring to target_model 'hivhistorycd4' will be overwritten.


to the bucket.py in the app add something like this::


    class HivHistoryBucket(ModelBucket):
        
        has_cd4 = ScheduledModelRule(                                        
            logic = (('has_cd4', 'equals', 'yes'), 'new', 'not_required'),     
            target_model = ['hivhistorycd4'] ,
            visit_model_fieldname = 'maternal_visit',
             )
        
        arv = ScheduledModelRule(
            logic = ((('on_cont_arv', 'equals', 'yes'),('init_arv', 'equals', 'yes', 'or')), 'new', 'not_required'), 
            target_model = ['hivhistoryarv'],
            visit_model_fieldname = 'maternal_visit',
             )
        
        class Meta:
            app_label = 'maikalelo_maternal'    
        
    bucket.register(HivHistory, HivHistoryBucket)
    
    
    class ObHistoryBucket(ModelBucket):
        
        is_hiv_pos = ScheduledModelRule(
            reference_model = ('maikalelo_maternal','maternalenrollment',),
            reference_model_filter = 'registered_subject',
            logic = (('is_hiv_pos', 'equals', 'yes'), 'new', 'not_required'),  
            target_model = ['demographichiv','deliveryhiv','hivhistory',
                            'hivhistorycd4', 'hivhistoryvl','hivhistorytest', 'hivhistoryarv'],
            visit_model_fieldname = 'maternal_visit',
             ) 
           
        class Meta:
            app_label = 'maikalelo_maternal'    
         
    bucket.register(ObHistory, ObHistoryBucket)