import pyodbc
from django.conf import settings
from bhp_actg_reference.models import Appendix40


def ImportAppendix(**kwargs):
    
    """Import records in old dmis for appendix 40
    After this, go to bhp_code_lists.utils """

    cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHP")
    cursor = cnxn.cursor()
    sql = "SELECT [refcode] as code, [shortdesc] as short_description, [description] as full_description FROM bhp.[dbo].[actg_app40]"
    cursor.execute(sql)
    for row in cursor:
        code = row.code.strip(' \t\n\r')
        short_description = row.short_description
        full_description = row.full_description
        if not Appendix40.objects.filter(code=code):
            Appendix40.objects.create(
                code = code,
                short_description = short_description,
                full_description = full_description,
                )
            print code    
