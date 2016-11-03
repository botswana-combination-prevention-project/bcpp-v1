from django.conf import settings


class Conf(object):

    @staticmethod
    def get(key, return_exception=False):
        try:
            return getattr(settings, key)
        except AttributeError:
            if return_exception:
                raise AttributeError('The settings file has no attribute: "{}"'.format(key))
            return None
