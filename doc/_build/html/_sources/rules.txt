Building Model Rules
====================

A Simple Example
----------------

        
Another Example
----------------


A Slightly Complicate Example
------------------------------
      

Rules are attributes of a RuleGroup
-------------------------------------

The rules are added as attributes to a subclass of :class:`~bhp_entry_rules.classes.rule_group.RuleGroup` like this::
    
    class HivHistoryRuleGroup(RuleGroup):
    
        rule = ....
        
        rule = ....
        
        class Meta:
            app_label = ....
            filter_model = ....
            source_model = ...       

RuleGroups are declared in a module or :file:`rule_groups.py` 
-------------------------------------------------------------

RuleGroups are declared in :file:`rule_groups.py`. Place the file in the root of your app. 


By Default, Rules Evaluate When the Dashboard is refreshed
-----------------------------------------------------------

The rules in a class evaluate when the dashboard is refreshed. 

Rules Evaluate in Order
-----------------------

