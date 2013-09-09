from lab_aliquot.models import Aliquot
from bhp_variables.models import StudySpecific


def AllocateAliquotIdentifier(user, aliquot_type):

    obj = StudySpecific.objects.all()[0]
    aliquot = Aliquot.objects.order_by('-id_int')
    if aliquot.count() > 0:
        seed = aliquot[0].id_seed + 1
    else:
        seed = obj.aliquot_seed
    id_int = 10000 + seed
    check_digit = id_int % 103
    while check_digit > 99:
        id_int += id_int
        seed += seed
        check_digit = id_int % 103
    aliquot_identifier = {}
    if check_digit < 10:
        aliquot_identifier['id'] = "0%s%s" % (id_int, check_digit)
    if check_digit >= 10 and check_digit < 100:
        aliquot_identifier['id'] = "%s%s" % (id_int, check_digit)
    aliquot_identifier['id_seed'] = seed
    aliquot_identifier['id_int'] = id_int
    if aliquot_type < 10:
        aliquot_type = "%s%s" % ('0', aliquot_type)
    aliquot_identifier['id'] = "%s%s%s%s" % (aliquot_identifier['id'], '0000', aliquot_type, '01')
    return aliquot_identifier
