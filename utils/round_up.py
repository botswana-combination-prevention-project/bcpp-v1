from decimal import Decimal, ROUND_HALF_UP

def round_up(d, digits):
    try:
        return Decimal(d).quantize(Decimal("1") / (Decimal('10') ** digits), ROUND_HALF_UP) 
    except:
        return d  
