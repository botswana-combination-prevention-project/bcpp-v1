.. automodule:: lab_tracker.classes

Classes
================== 

.. autoclass:: lab_tracker.classes.History
    :members:    
    :show-inheritance:

.. autoclass:: lab_tracker.classes.SiteTracker
    :members:
    :show-inheritance:    

The global `tracker` is an instance of :class:`SiteTracker` which is referred to in the :file:`tracker.py`::

    tracker.register(SubjectHivResult, HivHistory)