#!/usr/bin/env python

__author__ = 'Pranav Prakash <pranav@myblive.com>'

#   A Script that polls a MySQL Server and returns a status
#   which tells if the server is responding (active) or not
#   (inactive)


import sys
import os
import socket
from django.conf import settings


HOST = settings.DATABASES['lab_api']['HOST']
PORT = settings.DATABASES['lab_api']['PORT']

CURR_DIR = os.path.dirname(__file__)
LOGFILE = os.path.join(CURR_DIR, 'poll.log')


class PollMySQL(object):
    def __init__(self, host=None, port=None, **kwargs):
        if kwargs.get('db', None):
            db = kwargs.get('db')
            if not settings.DATABASES[db]['HOST']:
                self.host = '127.0.0.1'
            else:
                self.host = settings.DATABASES[db]['HOST']
            if not settings.DATABASES[db]['PORT']:
                self.port = 3306
            else:
                self.port = int(settings.DATABASES[db]['PORT'])
        else:
            self.host = host
            self.port = port
        self.server_response = False

    def poll(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
            s.send('ping')
            data = s.recv(1024)
            if data != '' and data is not None:
                self.server_response = True
        except:
            pass

    def is_server_active(self):
        self.poll()
        return self.server_response


def main(argv):

    host = HOST or argv[1]
    port = PORT or argv[2]
    if host and port:
        server_activity = PollMySQL(host, port).is_server_active()
        print server_activity
    else:
        show_help()
        sys.exit(0)


def show_help():
    """
        Shows a help about how to use this particular
        polling script
    """
    print """Usage: ./polling.py [HOST] [PORT]

        HOST: The HOST of the server
        PORT: The PORt used for MySQL Server
    """

if __name__ == '__main__':
    main(sys.argv)
