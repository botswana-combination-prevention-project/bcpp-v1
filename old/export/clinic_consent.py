import pymssql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from bhp066.apps.bcpp_clinic.models import ClinicConsent as EdcClinicConsent
from bhp066.apps.bcpp_subject.models import SubjectConsent as EdcSubjectConsent


class ClinicConsent(object):
    """ df_clinic = ClinicConsent().df """
    def __init__(self):
        qs = EdcClinicConsent.objects.all()
        columns = qs[0].__dict__.keys()
        columns.remove('_state')
        columns.append('household_member__household_structure__survey__survey_slug')
        columns.append('household_member__household_structure__household__plot__community')
        qs = EdcClinicConsent.objects.values_list(*columns).all()
        df = pd.DataFrame(list(qs), columns=columns)
        df.rename(columns={
            'household_member__household_structure__survey__survey_slug': 'survey',
            'household_member__household_structure__household__plot__community': 'community',
        }, inplace=True)
        df.fillna(value=np.nan, inplace=True)
        df['pims_identifier'] = df['pims_identifier'].str.strip()
        df['htc_identifier'] = df['htc_identifier'].str.strip()
        df['lab_identifier'] = df['lab_identifier'].str.strip()
        df.replace('', np.nan, inplace=True)
        df['lab_identifier'] = df['lab_identifier'].str.replace('-', '')
        df['htc_identifier'] = df['htc_identifier'].str.replace('-', '')
        for column in list(df.select_dtypes(include=['datetime64[ns, UTC]']).columns):
            df[column] = df[column].astype('datetime64[ns]')
        self.df = df
