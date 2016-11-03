import pymssql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from edc.subject.registration.models import RegisteredSubject as EdcRegisteredSubject


class RegisteredSubject(object):
    def __init__(self):
        qs = EdcRegisteredSubject.objects.all()
        columns = qs[0].__dict__.keys()
        columns.remove('_state')
        columns.remove('_user_container_instance')
        columns.remove('using')
        qs = EdcRegisteredSubject.objects.values_list(*columns).all()
        df = pd.DataFrame(list(qs), columns=columns)
        for column in list(df.select_dtypes(include=['datetime64[ns, UTC]']).columns):
            df[column] = df[column].astype('datetime64[ns]')
        df.fillna(value=np.nan, inplace=True)
        df.replace('', np.nan, inplace=True)
        self.df = df
