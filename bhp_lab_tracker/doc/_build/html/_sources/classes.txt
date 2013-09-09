.. automodule:: bhp_lab_tracker.classes

Classes
================== 

:class:`LabTracker` subclasses are defined in a module specific file :file:`lab_tracker.py`. Using 
:func:`bhp_lab_tracker.classes.Controller.site_lab_tracker.autodiscover`, :class:`LabTracker` subclasses are registered and made available
through a global :attr:`site_lab_tracker`. 

To get the value being tracked for a subject,  access :func:`site_lab_tracker.get_value`.

.. autoclass:: controller.Controller
    :members:
    :show-inheritance:
    :private-members:

.. autoclass:: tracker.LabTracker
    :members:    
    :show-inheritance:
    :private-members:
    
.. autoclass:: history_updater.HistoryUpdater
    :members:    
    :show-inheritance:
    :private-members:

.. note:: The global `site_lab_tracker` is an instance of :class:`Controller`.
    
Custom Subclasses of LabTracker
+++++++++++++++++++++++++++++++

.. autoclass:: hiv_lab_tracker.HivLabTracker
    :members:    
    :show-inheritance:
    :private-members: