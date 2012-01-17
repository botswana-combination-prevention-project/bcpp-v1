import socket
import settings


class TransactionProducer(object):
    
    def __init__(self):
        self.value = '%s-%s' % ( socket.gethostname().lower(),settings.DATABASES['default']['NAME'].lower())
        if len(self.value) > 25:
            raise ValueError('Transaction Producer name cannot exceed 25 characters.(hostname + settings.DATABASES[\'default\'][\'NAME\'])')
    def __get__(self, instance, owner):
        return self.value
        
    def __str__(self):
        return self.value

