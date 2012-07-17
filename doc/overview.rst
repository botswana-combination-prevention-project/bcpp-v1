Overview
========

Usually, at the beginning of a scheduled visit, all **scheduled** models are *required*. But conditions arise during the 
collection of data that might change that. :mod:`bhp_bucket` allows you to create rules that detect these conditions 
and change a model's entry status. For example, the status may change from *required* to *not required*. 

There also may be data conditions that suggest **additional** models are required that were not part of the original schedule
of data for the visit. :mod:`bhp_bucket` also allows you to create rules that detect these conditions 
and add the **additional** model or update the status of the **additional** model entry.

Previously, we placed the logic that manipulates the status of **scheduled** and **additional** models
in the :file:`forms.py`. This worked fine for data collected after the rule was added. The problem arose when rules were added after 
data collection had already begun. We needed a way to run the newly added rules on existing data without manually saving through all
the models via the user interface.

With :mod:`bhp_bucket`, all the rules for an application are dumped into one **bucket**, the :file:`bucket.py` and can be re-run programatically 
at any time.

The **scheduled** and **additional** model entry status values manipulated by the :mod:`bhp_bucket` :class:`ModelRule` are field attributes 
of models :class:`~bhp_entry.models.ScheduledBucketEntry` and :class:`~bhp_entry.models.ScheduledBucketEntry`. 
See :mod:`bhp_entry` for more details.



