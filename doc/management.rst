.. automodule:: lab_import_dmis.management

Management
==========

Tools
++++++

* import_dmis

To import results for a protocol from the DMIS into the django-lis, run the following from the source folder of the project::

    python manage.py import_dmis --import

.. note:: To import from the django-lis to the EDC, see module :mod:`lab_import_lis`.

Classes
+++++++

.. autoclass:: lab_import_dmis.management.commands.import_dmis.Command
    :members:
    :show-inheritance: 
