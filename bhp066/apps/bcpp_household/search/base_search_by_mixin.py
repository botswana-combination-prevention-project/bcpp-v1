from django.conf import settings


class BaseSearchByMixin(object):

    def get_most_recent_query_options(self):
        """Returns a dictionary to be added to the options for filtering the search model."""
        return {'community': settings.CURRENT_MAPPER}

    def get_current_community(self):
        """Returns the current community as configured in settings."""
        return settings.CURRENT_MAPPER
