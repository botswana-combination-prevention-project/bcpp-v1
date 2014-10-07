import csv

from collections import namedtuple

from ..models import SubjectRequisition

Result = namedtuple('Result', ('specimen_identifier subject_identifier received_date '
                               'specimen_condition assay_date utest_id result quantifier '
                               'requisition_identifier drawn_datetime'))


def import_from_dmis(path):
    """Does nothing"""
    results = []
    with open(path, 'rU') as f:
        header = None
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            if not header:
                header = row
                continue
            results.append(Result(*row + [None, None]))
    for result in results:
        try:
            subject_requisition = SubjectRequisition.objects.get(specimen_identifier=result.specimen_identifier)
            result.requisition_identifier = subject_requisition.requisition_identifier
            result.drawn_datetime = subject_requisition.drawn_datetime
        except SubjectRequisition.DoesNotExist:
            pass
    return results
