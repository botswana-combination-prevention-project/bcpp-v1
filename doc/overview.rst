Overview
========   

Module :mod:`bhp_crypto` provides model field classes that use either RSA or AES encryption depending 
on the length of the text field required. Not all field classes use the same encryption keys, so 
field value types can be grouped by the key pair used and access to un-encrypted values can be managed 
according to these groupings.

.. note:: Field level encryption protects data at rest but by itself is not sufficient to protect a system. Any project that uses :mod:`bhp_crypto` should be deployed on a system that uses full-drive encryption and the best of BIOS and OS level security features. 