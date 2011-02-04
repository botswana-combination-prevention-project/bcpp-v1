from models import LabAliquot

def AllocateAliquotIdentifier(user, lab_aliquot_type): 

    #get id in reverse order and select the top 1 int
    aliquot = LabAliquot.objects.order_by('-id_int')
    if aliquot.count() > 0:
        seed = aliquot[0].id_seed+1
    else: 
        seed = ALIQUOT_SEED   
    
    id_int = 10000 + seed
    check_digit = id_int % 103

    while check_digit > 99:
        id_int=id_int + 1
        seed = seed +1
        check_digit = id_int % 103
    aliquot_identifier = {}

    if check_digit <10:
        aliquot_identifier['id'] = "0%s%s" % ( id_int, check_digit )
    if check_digit >=10 and check_digit < 100:
        aliquot_identifier['id'] = "%s%s" % ( id_int, check_digit )
        
    aliquot_identifier['id_seed'] = seed
    aliquot_identifier['id_int'] = id_int
    
    if lab_aliquot_type < 10:
        lab_aliquot_type = "%s%s" % ('0', lab_aliquot_type)
    
    aliquot_identifier['id'] = "%s%s%s%s" % (aliquot_identifier['id'], '0000', lab_aliquot_type, '01')
    
    return aliquot_identifier
