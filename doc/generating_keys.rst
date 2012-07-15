Generating Keys
===============

.. warning:: Keys should be safely stored and properly backed up.
 
The EDC is often deployed on disconnected mobile devices. In this environment the keys are stored on the device inside a mountable *truecrypt* file 
(see also :doc:`protecting_keys_with_truecrypt`). 

Use the *settings* attribute *KEY_PATH* to indicate the location of the mounted truecrypt file::

    KEY_PATH='/Volume/project_keys/keys'

With the KEY_PATH attribute set, generate new keys::

    from bhp_crypto.utils import setup_new_keys()
    setup_new_keys()
         
The new keys will be in the folder::

    user-aes-local          
    user-encrypted-salt     
    user-public-irreversible.pem
    user-public-restricted.pem
    user-private-restricted.pem
    user-public-local.pem
    user-private-local.pem      
    
