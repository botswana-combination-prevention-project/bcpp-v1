from django.contrib import admin
from django.utils.translation import ugettext as _

from ..forms import MonthsRecentPartnerForm, MonthsSecondPartnerForm, MonthsThirdPartnerForm
from ..models import MonthsRecentPartner, MonthsSecondPartner, MonthsThirdPartner

from .subject_visit_model_admin import SubjectVisitModelAdmin


class MonthsRecentPartnerAdmin(SubjectVisitModelAdmin):

    form = MonthsRecentPartnerForm
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'partner_hiv_test',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)
    exclude = ('first_partner_arm', )
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "sex_partner_community": admin.VERTICAL,
        "past_year_sex_freq": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "first_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
    instructions = [(
        "Interviewer Note: Ask the respondent to answer"
        " the following questions about their most recent"
        " sexual partner in the past 12 months. It may be"
        " helpful for respondent to give initials or"
        " nickname, but DO NOT write down or otherwise"
        "record this information. "),
        _("Read to Participant: I am now going to ask you"
          " about your most recent sexual partners. I will"
          " start with your last or most recent sexual partner.")]
admin.site.register(MonthsRecentPartner, MonthsRecentPartnerAdmin)


class MonthsSecondPartnerAdmin(SubjectVisitModelAdmin):
    # NOTE: this is not a supplemental form, it should be filled in based on the responses in SecondPartner.
    form = MonthsSecondPartnerForm
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'partner_hiv_test',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)
    exclude = ('second_partner_arm', )
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "sex_partner_community": admin.VERTICAL,
        "past_year_sex_freq": admin.VERTICAL,
        "first_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
    instructions = [(
        "Interviewer Note: If the respondent has only had "
        " one partner, SKIP to HIV adherence questions if HIV"
        " negative. Else go to Reproductive health for women,"
        " or circumcision for men. Ask the respondent to"
        " answer the following questions about their second"
        " most recent sexual partner. It may be helpful for"
        " respondent to give initials or nickname, but DO NOT"
        " write down or otherwise record this information."),
        _("Read to Participant: I am now going to ask you about"
          " your second most recent sexual partner in the past,"
          "the one before the person we were just talking about.")]

admin.site.register(MonthsSecondPartner, MonthsSecondPartnerAdmin)


class MonthsThirdPartnerAdmin(SubjectVisitModelAdmin):

    form = MonthsThirdPartnerForm
    fields = (
        "subject_visit",
        'first_partner_live',
        'third_last_sex',
        'third_last_sex_calc',
        'first_first_sex',
        'first_first_sex_calc',
        'first_sex_current',
        'first_relationship',
        'first_exchange',
        'concurrent',
        'goods_exchange',
        'first_sex_freq',
        'first_partner_hiv',
        'partner_hiv_test',
        'first_haart',
        'first_disclose',
        'first_condom_freq',
        'first_partner_cp',)

    exclude = ('third_partner_arm', )
    radio_fields = {
        "third_last_sex": admin.VERTICAL,
        "first_first_sex": admin.VERTICAL,
        "first_sex_current": admin.VERTICAL,
        "first_relationship": admin.VERTICAL,
        "concurrent": admin.VERTICAL,
        "goods_exchange": admin.VERTICAL,
        "sex_partner_community": admin.VERTICAL,
        "past_year_sex_freq": admin.VERTICAL,
        "first_exchange": admin.VERTICAL,
        "first_partner_hiv": admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        "first_haart": admin.VERTICAL,
        "first_disclose": admin.VERTICAL,
        "first_condom_freq": admin.VERTICAL,
        "first_partner_cp": admin.VERTICAL, }
    filter_horizontal = ("first_partner_live",)
    instructions = [(
        "<H5>Interviewer Note</H5> If the respondent has only had "
        " two partners, SKIP HIV adherence questions if HIV"
        " negative, if HIV positive, proceed. Else go to Reproductive health for women,"
        " or circumcision for men. Ask the respondent to"
        " answer the following questions about their second"
        " most recent sexual partner. It may be helpful for"
        " respondent to give initials or nickname, but DO NOT"
        " write down or otherwise record this information."
    ),
        _("<H5>Read to Participant</H5> I am now going to ask you about"
          "your second most recent sexual partner in the past"
          " 12 months, the one before the person we were just"
          "talking about.")]
admin.site.register(MonthsThirdPartner, MonthsThirdPartnerAdmin)
