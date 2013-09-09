Importing Data
===============

It is important for an Edc installation to retrieve lab data from the Lis.

set up a cronjob::

    */10 6-22/1 * * * /etc/cron.daily/edc_update_labs.sh >> /tmp/edc_update_labs
    
where file :file:`edc_update_labs.sh` calls the management command `import_lis`. For example, 
if the :file:`settings.py` is in `/home/django/source/bhp056`::

    cd /home/django/source/bhp056 && \
    python manage.py import_dmis --import && \
    python manage.py import_lis --import

