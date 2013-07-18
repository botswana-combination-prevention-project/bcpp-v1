import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import BaselineHouseholdSurvey


class BaselineHouseholdSurveyFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaselineHouseholdSurvey

    report_datetime = datetime.today()
    flooring_type = (('Dirt/earth', 'Dirt/earth '), ('Wood, plank', 'Wood, plank'), ('Parquet/lino', 'Parquet/lino'), ('Cement', 'Cement'), ('Tile flooring', 'Tile flooring'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    flooring_type_other = factory.Sequence(lambda n: 'flooring_type_other{0}'.format(n))
    water_source = (('Communal tap', 'Communal tap'), ('Standpipe/tap within plot', 'Standpipe/tap within plot'), ('Piped indoors', 'Piped indoors'), ('Borehore', 'Borehole'), ('Protected well', 'Protected well'), ('Unprotected/shallow well', 'Unprotected/shallow well'), ('River /dam/lake/pan', 'River /dam/lake/pan'), ('Bowser/tanker', 'Bowser/tanker'), ('OTHER', 'Other, specify (including unknown):'), ("Don't want to answer", "Don't want to answer"))[0][0]
    water_source_other = factory.Sequence(lambda n: 'water_source_other{0}'.format(n))
    energy_source = (('Charcoal/wood', 'Charcoal/wood'), ('Paraffin', 'Paraffin'), ('Gas', 'Gas'), ('Electricity (mains)', 'Electricity (mains)'), ('Electricity (solar)', 'Electricity (solar)'), ('No cooking done', 'No cooking done'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    energy_source_other = factory.Sequence(lambda n: 'energy_source_other{0}'.format(n))
    toilet_facility = (('Pit latrine within plot', 'Pit latrine within plot'), ('Flush toilet within plot', 'Flush toilet within plot'), ("Neighbour's flush toilet", "Neighbour's flush toilet"), ("Neighbour's pit latrine", 'Neighbours pit latrine'), ('Communal flush toilet', 'Communal flush toilet'), ('Communal pit latrine', 'Communal pit latrine'), ('Pail bucket latrine', 'Pail bucket latrine'), ('Bush', 'Bush'), ('River or other body of water', 'River or other body of water'), ('OTHER', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    toilet_facility_other = factory.Sequence(lambda n: 'toilet_facility_other{0}'.format(n))
    smaller_meals = (('Never', 'Never'), ('Rarely', 'Rarely'), ('Sometimes', 'Sometimes'), ('Often', 'Often'), ("Don't want to answer", "Don't want to answer"))[0][0]
