from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from ..models import HtcRecentPartner, HtcSecondPartner, HtcThirdPartner
from ..forms import HtcRecentPartnerForm, HtcSecondPartnerForm, HtcThirdPartnerForm


class HtcRecentPartnerAdmin(HtcSubjectVisitModelAdmin):

    form = HtcRecentPartnerForm

    fields = (
        "htc_subject_visit",
        "report_datetime",
        "recent_partner_rel",
        "partner_tested",
        "parter_status",
        "partner_residency",
    )
    radio_fields = {
        "recent_partner_rel": admin.VERTICAL,
        "partner_tested": admin.VERTICAL,
        "parter_status": admin.VERTICAL,
        "partner_residency": admin.VERTICAL}
    instructions = [("Read to Participant: Now I will ask some questions about"
                     " sex and sex partners.  Some of these questions may make"
                     " you uncomfortable; however, please remember that your"
                     " answers are confidential and it is really important for"
                     " us to get the most honest answer you can give us."
                     "  In this set of questions, when I say sex, I mean"
                     " vaginal or anal sex.  I do not mean oral sex, kissing,"
                     " or touching with hands.  When I say a partner, I mean"
                     " anyone you might have had sex with.  Partners can be"
                     " your husband, wife or wives, girlfriends, boyfriends,"
                     " friends, casual partners, prostitutes, or someone you"
                     " may have met at a bar, or at a wedding or other special"
                     " events, etc.")]
admin.site.register(HtcRecentPartner, HtcRecentPartnerAdmin)


class HtcSecondPartnerAdmin(HtcSubjectVisitModelAdmin):

    form = HtcSecondPartnerForm

    fields = (
        "htc_subject_visit",
        "report_datetime",
        "second_partner_rel",
        "partner_tested",
        "parter_status",
        "partner_residency",
    )
    radio_fields = {
        "second_partner_rel": admin.VERTICAL,
        "partner_tested": admin.VERTICAL,
        "parter_status": admin.VERTICAL,
        "partner_residency": admin.VERTICAL}
    instructions = [("Read to Participant: Now I will ask some questions about"
                     " sex and sex partners.  Some of these questions may make"
                     " you uncomfortable; however, please remember that your"
                     " answers are confidential and it is really important for"
                     " us to get the most honest answer you can give us."
                     "  In this set of questions, when I say sex, I mean"
                     " vaginal or anal sex.  I do not mean oral sex, kissing,"
                     " or touching with hands.  When I say a partner, I mean"
                     " anyone you might have had sex with.  Partners can be"
                     " your husband, wife or wives, girlfriends, boyfriends,"
                     " friends, casual partners, prostitutes, or someone you"
                     " may have met at a bar, or at a wedding or other special"
                     " events, etc.")]
admin.site.register(HtcSecondPartner, HtcSecondPartnerAdmin)


class HtcThirdPartnerAdmin(HtcSubjectVisitModelAdmin):

    form = HtcThirdPartnerForm

    fields = (
        "htc_subject_visit",
        "report_datetime",
        "third_partner_rel",
        "partner_tested",
        "parter_status",
        "partner_residency",
    )
    radio_fields = {
        "third_partner_rel": admin.VERTICAL,
        "partner_tested": admin.VERTICAL,
        "parter_status": admin.VERTICAL,
        "partner_residency": admin.VERTICAL}
    instructions = [("Read to Participant: Now I will ask some questions about"
                     " sex and sex partners.  Some of these questions may make"
                     " you uncomfortable; however, please remember that your"
                     " answers are confidential and it is really important for"
                     " us to get the most honest answer you can give us."
                     "  In this set of questions, when I say sex, I mean"
                     " vaginal or anal sex.  I do not mean oral sex, kissing,"
                     " or touching with hands.  When I say a partner, I mean"
                     " anyone you might have had sex with.  Partners can be"
                     " your husband, wife or wives, girlfriends, boyfriends,"
                     " friends, casual partners, prostitutes, or someone you"
                     " may have met at a bar, or at a wedding or other special"
                     " events, etc.")]
admin.site.register(HtcThirdPartner, HtcThirdPartnerAdmin)
