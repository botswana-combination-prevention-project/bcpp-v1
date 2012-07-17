Building Model Rules
====================

A Simple Example
----------------

A simple rule might look like this::

    has_cd4 = ScheduledModelRule(
        logic = (('has_cd4', 'equals', 'yes'), 'new', 'not_required'),
        target_model = ['hivhistorycd4'] ,
         )

This is a rule that sets the entry status of a a **scheduled** model to either **required** or **not required**. 
The **scheduled** model is the :attr:`target_model` :class:`HiVHistoryCd4`. The :attr:`logic` attribute is a tuple 
of (**predicate**, **consequent**, **alternative**) which will resolve into::

    if hiv_history_cd4.has_cd4=='yes':
        scheduled_entry_bucket.status='new'
    else:
        scheduled_entry_bucket.status='not_required'
        
Another Example
----------------
.. code-block:: python

    arv = ScheduledModelRule(
        logic = ((('on_cont_arv', 'equals', 'yes'),('init_arv', 'equals', 'yes', 'or')), 'new', 'not_required'), 
        target_model = ['hivhistoryarv'],
         )
             
The logic attribute is still a tuple of (**predicate**, **consequent**, **alternative**) but the **predicate** is
now a tuple of tuples where the second tuple has an extra element **or**.

The resolved code would be::

    if hiv_history_cd4.has_cd4=='yes' or hiv_history_cd4.init_arv=='yes':
        scheduled_entry_bucket.status='new'
    else:
        scheduled_entry_bucket.status='not_required'

A Slightly Complicate Example
------------------------------
      
It may be that the field attribute in **predicate** of the :attr:`logic` tuple does not come from the :attr:`target_model`
and/or the rule is to change the entry status of more than one target model. In the examples above, the target model and the 
model used in the predicate were the same. The model used in the **predicate** is the **reference model** and in most cases it is
the same model as the target model so you do not need to explicitly set the :attr:`reference_model` attribute. But when it 
is not the same or the target model is more than one, you need to set :attr:`reference_model`. 

:attr:`reference_model` is a tuple of (app_label, model_name). The reference model must have a foreign key to either the
**visit model** or **registered_subject**::

    is_hiv_pos = ScheduledModelRule(
        reference_model = ('maikalelo_maternal','maternalenrollment',),
        logic = (('is_hiv_pos', 'equals', 'yes'), 'new', 'not_required'),  
        target_model = ['demographichiv','deliveryhiv','hivhistory',
                        'hivhistorycd4', 'hivhistoryvl','hivhistorytest', 'hivhistoryarv'],
         )
  
...will resolve to something like::

    for model_name in target_model:
        if maternal_enrollment.is_hiv_positive=='yes':
           scheduled_entry_bucket.status='new'
        else:
           scheduled_entry_bucket.status='new'
                     

Note that the model rules have access to the **visit model** of the current visit.

Rules are attributes of a ModelBucket
-------------------------------------

The rules are added as attributes to a subclass of :class:`~bhp_bucket.classes.model_bucket.ModelBucket` like this::
    
    class HivHistoryBucket(ModelBucket):
    
        rule = ....
        
        rule = ....
        
        class Meta:
            app_label = ....
            visit_model = ....

A ModelBucket is Registered to `bucket` with a Model
----------------------------------------------------
The class is registered with bucket along with a model like this::

    bucket.register(HivHistory, HivHistoryBucket)

The rules will be evaluated when the model is saved, in this case, **HivHistory**.          

ModelBuckets are declared in :file:`bucket.py` 
----------------------------------------------

ModelBuckets are declared in :file:`bucket.py`. Place the file in the root of your app. 


By Default, Rules Evaluate When the Model is Saved
--------------------------------------------------

The rules in a class evaluate when the model the class was registered with is saved. But the rules can also be
evaluated programatically.

Rules Evaluate in Order
-----------------------

The order in which the model bucket classes are listed matters and the order of the rules within the model bucket class
matters. If rules refer to the same model, only the result of the last rule will matter. In the example below, 
the target_model 'hivhistorycd4' is referred to in HivHistoryBucket and ObHistoryBucket.
Since ObHistoryBucket rules will run last, the result of the HivHistoryBucket
rule referring to target_model 'hivhistorycd4' will be overwritten.

To the :file:`bucket.py` in the app add something like this::

    class HivHistoryBucket(ModelBucket):
        
        has_cd4 = ScheduledModelRule(                                        
            logic = (('has_cd4', 'equals', 'yes'), 'new', 'not_required'),     
            target_model = ['hivhistorycd4'] ,
             )
        
        arv = ScheduledModelRule(
            logic = ((('on_cont_arv', 'equals', 'yes'),('init_arv', 'equals', 'yes', 'or')), 'new', 'not_required'), 
            target_model = ['hivhistoryarv'],
             )
        
        class Meta:
            app_label = 'maikalelo_maternal'    
            visit_model = 'maternal_visit',
        
    bucket.register(HivHistory, HivHistoryBucket)
    
    
    class ObHistoryBucket(ModelBucket):
        
        is_hiv_pos = ScheduledModelRule(
            reference_model = ('maikalelo_maternal','maternalenrollment',),
            reference_model_filter = 'registered_subject',
            logic = (('is_hiv_pos', 'equals', 'yes'), 'new', 'not_required'),  
            target_model = ['demographichiv','deliveryhiv','hivhistory',
                            'hivhistorycd4', 'hivhistoryvl','hivhistorytest', 'hivhistoryarv'],
             ) 
           
        class Meta:
            app_label = 'maikalelo_maternal'  
            visit_model = 'maternal_visit',
              
         
    bucket.register(ObHistory, ObHistoryBucket)