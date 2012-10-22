.. automodule:: bhp_lab_tracker.classes

Classes
================== 

.. autoclass:: bhp_lab_tracker.classes.LabTracker
    :members:    
    :show-inheritance:

.. autoclass:: bhp_lab_tracker.classes.SiteLabTracker
    :members:
    :show-inheritance:    

The global `lab_tracker` is an instance of :class:`SiteLabTracker` which is referred to in the :file:`lab_tracker.py`::

    lab_tracker.register(SubjectHivResult, HivHistory)
    
Custom Subclasses of LabTracker
+++++++++++++++++++++++++++++++

.. autoclass:: bhp_lab_tracker.classes.HivLabTracker
    :members:    
    :show-inheritance: