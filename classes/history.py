from lab_clinic_api.models import ResultItem
from lab_tracker.models import HistoryModel


class History(object):

    def __init__(self):
        self.value_map = self._get_value_map()

    def update_now(self, subject_identifier):
        """Just updates the history values."""
        self._update(subject_identifier)

    def get(self, subject_identifier, order_desc=False):
        """Returns all values as a ordered queryset."""
        order_by = 'value_datetime'
        if order_desc:
            order_by = '-{0}'.format(order_by)
        test_key = self._update(subject_identifier)
        return HistoryModel.objects.filter(subject_identifier=subject_identifier, test_key=test_key).order_by(order_by)

    def get_current_value(self, subject_identifier):
        """Returns only the most current value."""
        queryset = self.get(subject_identifier, True)
        if queryset:
            return queryset[0].value
        else:
            return None

    def get_as_list(self, subject_identifier):
        """Returns all values as a list in ascending chronological order."""
        queryset = self.get(subject_identifier)
        return [qs.value for qs in queryset]

    def get_as_string(self, subject_identifier, mapped=True):
        """Returns a subject's qualitative values joined as a string in ascending chronological order.

        If mapped is True and a value_map is defined, map is inverted and a string of values is generated from the map."""
        if not self.value_map:
            mapped = False
        retlst = []
        inv_value_map = {}
        lst = self.get_as_list(subject_identifier)
        if mapped:
            for k, v in self.value_map.iteritems():
                inv_value_map[v] = inv_value_map.get(v, [])
                inv_value_map[v].append(k)
        for l in lst:
            if mapped:
                retlst.append(inv_value_map[l][0].lower())
            else:
                retlst.append(l)
        return ''.join(retlst)

    def get_prep(self):
        """Returns a tuple of (test_code, test_key) where test_code may be a list.

        This method defines:
          test_code: a list of test_codes to search for in :class:`ResultItem`.
          test_key: the common key for all instances of the HistoryModel for the subclass.

        Users should override this."""
        return ([], None)

    def update_prep(self, subject_identifier, test_key):
        """ Updates the HistoryModel if the user has other sources to include.

        Users may override."""
        pass

    def _update(self, subject_identifier):
        """Updates the HistoryModel with the subject's values."""
        test_code, test_key = self.get_prep()
        if not test_key:
            raise TypeError('Parameter \'test_key\' cannot be None. See method get_prep().')
        if not isinstance(test_code, list):
            test_code = [test_code]
        self.update_prep(subject_identifier, test_key)
        for result_item in ResultItem.objects.filter(result__subject_identifier=subject_identifier, test_code__code__in=test_code):
            defaults = {'value': result_item.result_item_value}
            history_model, created = HistoryModel.objects.get_or_create(subject_identifier=subject_identifier,
                                                                        test_key=test_key,
                                                                        test_code=result_item.test_code.code,
                                                                        value_datetime=result_item.result_item_datetime,
                                                                        defaults=defaults)
            if not created:
                if result_item.result:
                    history_model.value = result_item.result_item_value
                    history_model.save()
        return test_key

    def get_value_map_prep(self):
        """Returns a dictionary that may be used to map values for storage in the :class:`HistoryModel` to value formats used in :class:`ResultItem` model.

            Format {given this value: store this value}.

            This is useful if update_prep adds results that are not described in the same format as the :class:`ResultItem` model.

            For example:
                {'A': 'POS', 'B': NEG} will store POS and NEG given A, B. POS, NEG is how it is stored in the :class:`ResultItem` model.

            Also, the map is inverted to generate a string of values using this map returning 'AB' instead of 'POSNEG'.

            Users may override."""
        return {}

    def _get_value_map(self):
        """Gets and returns a value_map if one has been defined."""
        return self.get_value_map_prep()

    def update_history_model(self, **kwargs):
        """ Creates or Updates HistoryModel using get_or_create with kwargs."""
        defaults = kwargs.get('defaults')
        value = defaults.get('value')
        history_model, created = HistoryModel.objects.get_or_create(
            subject_identifier=kwargs.get('subject_identifier'),
            test_key=kwargs.get('test_key'),
            test_code=kwargs.get('test_code'),
            value_datetime=kwargs.get('value_datetime'),
            defaults=defaults)
        if not created:
            if value:
                history_model.result = self.value_map[value]
                history_model.save()
