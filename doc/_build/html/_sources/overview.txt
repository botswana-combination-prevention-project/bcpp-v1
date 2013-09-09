Overview
========

This module imports results from the DMIS into the django-lis. To avoid re-importing every result 
on every import session, the date and time of the import is recorded. When the next session starts,
the routine only looks for records after the last import date and time.

The import routine first tries to import anything with a receiving record after the last import datetime. 
Then looks for any related records that have been modified since the last import datetime. 
