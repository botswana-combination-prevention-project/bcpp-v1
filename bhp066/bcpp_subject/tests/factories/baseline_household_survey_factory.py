import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import BaselineHouseholdSurvey


class BaselineHouseholdSurveyFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaselineHouseholdSurvey

    report_datetime = datetime.today()
    flooring_type = (('Dirt/earth', u'Dirt/earth '), ('Wood, plank', u'Wood, plank'), ('Parquet/lino', u'Parquet/lino'), ('Cement', u'Cement'), ('Tile flooring', u'Tile flooring'), ('OTHER', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    flooring_type_other = factory.Sequence(lambda n: 'flooring_type_other{0}'.format(n))
    water_source = (('Communal tap', u'Communal tap'), ('Standpipe/tap within plot', u'Standpipe/tap within plot'), ('Piped indoors', u'Piped indoors'), ('Borehore', u'Borehole'), ('Protected well', u'Protected well'), ('Unprotected/shallow well', u'Unprotected/shallow well'), ('River /dam/lake/pan', u'River /dam/lake/pan'), ('Bowser/tanker', u'Bowser/tanker'), ('OTHER', u'Other, specify (including unknown):'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    water_source_other = factory.Sequence(lambda n: 'water_source_other{0}'.format(n))
    energy_source = (('Charcoal/wood', u'Charcoal/wood'), ('Paraffin', u'Paraffin'), ('Gas', u'Gas'), ('Electricity (mains)', u'Electricity (mains)'), ('Electricity (solar)', u'Electricity (solar)'), ('No cooking done', u'No cooking done'), ('OTHER', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    energy_source_other = factory.Sequence(lambda n: 'energy_source_other{0}'.format(n))
    toilet_facility = (('Pit latrine within plot', u'Pit latrine within plot'), ('Flush toilet within plot', u'Flush toilet within plot'), ("Neighbour's flush toilet", u"Neighbour's flush toilet"), ("Neighbour's pit latrine", u'Neighbours pit latrine'), ('Communal flush toilet', u'Communal flush toilet'), ('Communal pit latrine', u'Communal pit latrine'), ('Pail bucket latrine', u'Pail bucket latrine'), ('Bush', u'Bush'), ('River or other body of water', u'River or other body of water'), ('OTHER', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    toilet_facility_other = factory.Sequence(lambda n: 'toilet_facility_other{0}'.format(n))
    smaller_meals = (('Never', u'Never'), ('Rarely', u'Rarely'), ('Sometimes', u'Sometimes'), ('Often', u'Often'), ("Don't want to answer", u"Don't want to answer"))[0][0]
