Troubleshooting
===============

Sometimes results do not come through from the DMIS. 

First try triggering import by changing the modification datetime on the receiving record.
                 
  .. code-block:: python
     
     python manage.py import_dmis --flag_for_reimport <receive_identifier>
     
  followed by::
      
     python manage.py import_dmis --import


If that does not work, then a condition exists on the DMIS that this module cannot handle. Here are
some conditions we have seen.

1. Result is on the DMIS and validated but when looking at the validation batch the result is actually
accepted but "already on file". 

  .. note:: This means the result was already in the result table (LAB21/LAB21D) or "on file" when 
            the validation step was submitted. Perhaps the result was manually entered before
            validation. Manually entered results do not go through a validation step.

  .. seealso:: See comment on class :class:`Dmis`.

  Unvalidate the result using information from the validation batch.
      
  .. code-block:: python
     
     python manage.py import_dmis --unvalidate_on_dmis <batch> <resultset> <receive_identifier>
  
  Revalidate the item by going to the validation page on the DMIS for this batch.

  Once the item has been "sent" from the validation page, re-import::

    python manage.py import_dmis --import
    
      
  .. note:: The assay datetime and validation datetime on the final result might change
            to today's date. 
            
  .. note:: Data moves from validation batches to LAB21 using a SQL Server Agent job named
            "BHPLAB: move validated batches to LAB21". You may wish to start it. It usually
            runs every ten minutes.
                        
2. Result is accepted and sent but validation datetime and user are None
  
  You see a message like this::
  
    NOT RELEASING 1244494 resulted on 2011-05-25 (datetime:None, user:None)
 
  which means the validation information in L23 is not in sync with the result in LAB21. That is,
  the result_guids do not match.
  
  You may also see a warning that "L23.guid does not match L21.guid". If so,
  the validation information is for the same receiving identifier but does not
  match the result. If the sequence of validation is done without any manipulation, 
  these values should match.

  To correct, just follow the steps above in (1).