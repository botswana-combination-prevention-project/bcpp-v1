def AllocateResultItemIdentifier(result_identifier, cnt): 

    if cnt < 10:
        pad = '00'
    elif cnt>=10 and cnt < 100:
        pad = '0'
    else:
        pad = ''    
    
    return '%s-%s%s' % (result_identifier, pad, cnt)

