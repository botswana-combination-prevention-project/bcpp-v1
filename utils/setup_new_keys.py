__authors__ = [
    '"Erik van Widenfelt" <ew2789@gmail.com>',
]

import os
import sys
from datetime import datetime
from bhp_crypto.classes import Crypter


def setup_new_keys():

    """ Utility to generate all new keys for the project."""
    datestring = datetime.today().strftime('%Y%m%d%H%M%S%f')
    crypter = Crypter(no_preload=True)
    filenames = []
    for algorithm, value in crypter.VALID_MODES.iteritems():
        if not isinstance(value, dict):
            filenames.append(value)
        else:
            for filename in crypter.VALID_MODES.get(algorithm).itervalues():
                if not isinstance(filename, dict):
                    filenames.append(filename)
                else:
                    for filename in filename.itervalues():
                        filenames.append(filename)
    # backup existing keys
    try:
        path = 'keys_backup_{0}'.format(datestring)
        os.mkdir(path)
        print path
    except:
        raise TypeError('failed to create backup folder')
    for filename in filenames:
        try:
            oldpath = os.path.join(os.path.realpath('.'), filename)
            newpath = os.path.join(os.path.join(
                                       os.path.realpath('.'), path), filename)
            if os.path.exists(oldpath):
                os.rename(oldpath, newpath)
                print 'copied {0}'.format(filename)
        except OSError as e:
            print ('Failed to copy {0} to backup '
                  'folder {1}'.format(filename, path))
            break
    # confirm target folder has no keys
    old_keys_exist = False
    for filename in filenames:
        oldpath = os.path.join(os.path.realpath('.'), filename)
        if os.path.exists(oldpath):
            old_keys_exist = True
            break

    if old_keys_exist:
        print 'Failing. Old keys are still in the target folder. Try moving them manually.'
    else:
        print 'Creating new keys'
        del crypter
        crypter = Crypter(no_preload=True)
        crypter.create_new_rsa_key_pairs(suffix='')
        crypter.create_new_salt(suffix='')
        crypter.create_aes_key(suffix='')
        sys.stdout.flush()
