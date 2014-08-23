from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

BHS_START_DATE = date(2014, 8, 27)
BHS_FULL_ENROLLMENT_DATE = date(2014, 10, 7)
BHS_END_DATE = date(2014, 10, 21)
SMC_START_DATE = date(2014, 10, 15)
SMC_ECC_START_DATE = date(2014, 7, 10)

INTERVENTION_COMMUNITIES = [11, 13, 15, 17, 19, 21, 23, 25, 27, 29]

CLINIC_DAYS = {
    '11': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '12': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '13': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '14': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '15': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '16': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '17': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '18': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '19': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '20': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '21': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '22': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '23': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '24': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '25': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '26': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '27': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '28': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '29': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '30': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '31': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '32': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '33': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '34': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '35': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '36': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '37': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '38': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '39': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    '40': {'IDCC': ((MO, WE), ),
           'ANC': ((MO, TU, WE, TH, FR), ),
           'SMC': ((MO, TU, WE, TH, FR), SMC_START_DATE),
           'SMC-ECC': ((MO, TU, WE, TH, FR), SMC_ECC_START_DATE)},
    }
