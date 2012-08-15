

class BaseDmis(object):

    def get_receive_row_from_cursor(self, cursor):
        """ Holds the receiving record from the DMIS (LAB01). """
        attrs = {'__str__': lambda self: '{0} as of {1}'.format(cursor[1], cursor[13]),
                 'dmis_reference': cursor[0],
                'receive_identifier': cursor[1],
                'tid': cursor[2],
                 'condition': cursor[3],
                 'visit': cursor[4],
                 'site_identifier': cursor[5],
                 'protocol_identifier': cursor[6],
                'gender': cursor[7],
                'dob': cursor[8],
                'subject_identifier': cursor[9],
                'initials': cursor[10],
                'clinician_initials': cursor[11],
                'user_created': cursor[12],
                'user_modified': cursor[13],
                'receive_datetime': cursor[14],
                'drawn_datetime': cursor[15],
                'created': cursor[16],
                'modified': cursor[17],
                'order_identifier': cursor[18],
                'panel_id': cursor[19],
                'edc_specimen_identifier': cursor[20],
                'other_pat_ref': cursor[21],
                'site': None,
                'patient': None,
                'protocol': None}
        return type('ReceiveRow', (object,), attrs)

    def get_order_row_from_cursor(self, cursor):
        """ Holds the order record from the DMIS (LAB21). """
        attrs = {'__str__': lambda self: '{0} as of {1}'.format(cursor[18], cursor[13]),
                 'dmis_reference': cursor[0],
                'receive_identifier': cursor[1],
                'tid': cursor[2],
                'user_created': cursor[12],
                'user_modified': cursor[13],
                'order_datetime': cursor[15],
                'created': cursor[16],
                'modified': cursor[17],
                'order_identifier': cursor[18],
                'panel': None,
                'aliquot': None}
        return type('OrderRow', (object,), attrs)
