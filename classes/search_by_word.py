from bhp_search.classes.base_search_by_word import BaseSearchByWord


class SearchByWord(BaseSearchByWord):

    def get_search_prep_models(self):

        return {'subjectconsent': ('bcpp_subject', 'subjectconsent')}
