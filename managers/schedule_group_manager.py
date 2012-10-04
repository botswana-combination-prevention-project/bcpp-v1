import re
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import Q
#from bhp_visit.models import MembershipForm


class ScheduleGroupManager(models.Manager):

    def get_membership_forms_for(self, registered_subject, membership_form_category, **kwargs):

        """ Returns dict of keyed and unkeyed schedule group membership forms for agiven registered_subject

        Specify the registered_subject and the membership_form_category. Include forms
        of the specified membership_form__category AND those that have no category (null) or blank.
        """
        MembershipForm = models.get_model('bhp_visit', 'membershipform')
        # if this model is keyed, exclude all other UNKEYED models LIKE this from the list
        # for example, if consented, no other membership forms apply and
        # the links need not show on the dashboard
        exclude_others_if_keyed_model_name = kwargs.get("exclude_others_if_keyed_model_name", None)

        # TODO: implement 'include_after_exclusion_model_keyed'
        # ...not working yet because the query would be complicated
        # if the "exclude" model (above) is keyed, remove all unkeyed models, except those listed here
        # for example, if the model in 'exclude_others_if_keyed_model_name' is KEYED,
        # still show links to the models listed here
        # (naming needs work ...)
        # include_after_exclusion_model_keyed = kwargs.get("include_after_exclusion_model_keyed", None)
        # category of the membership form. Can be any value as  long as
        # it helps link membership forms in some way. For example,
        # to distinguish 'maternal' from 'infant' forms. Specified at the form level

        #  membership form 'category' should appear in the category field of membership_form.
        if not MembershipForm.objects.filter(category__iexact=membership_form_category).exists():
            raise ValueError('Can\'t find any membership forms! Have you configured any for category \'%s\'.' % membership_form_category)
        if not super(ScheduleGroupManager, self).filter(membership_form__category__iexact=membership_form_category).exists():
            raise ValueError('Can\'t find any schedule groups! Have you configured any for category \'%s\'.' % membership_form_category)

        # a list of "keys" that link like membership forms together. If they share this
        # key it means that only one form should be KEYED per subject.
        # If form is KEYED for subject, there is no need to list the others as UNKEYED
        # Specified at the scheduledgroup level
        grouping_keys = []
        # a list of KEYED forms
        keyed_membership_forms = {}
        #get KEYED schedule group membership forms
        for schedule_group in super(ScheduleGroupManager, self).filter(membership_form__category__iexact=membership_form_category):
            membership_form_model = schedule_group.membership_form.content_type_map.model_class()
            try:
                if membership_form_model.objects.filter(registered_subject_id=registered_subject.pk):
                    # append grouping key for schedule groups
                    # where the membership_form is KEYED and the schedule group
                    # has more than one membership_form
                    if schedule_group.grouping_key:
                        grouping_keys.append(schedule_group.grouping_key)
                    # add KEYED model
                    keyed_membership_forms.update({schedule_group.membership_form.content_type_map.name: membership_form_model.objects.get(registered_subject=registered_subject)})
            except FieldError:
                # raise error is attribute is missing
                raise FieldError('Membership forms require attribute \'registered_subject\'. Model \'%s\' does not have this attribute but is listed as a membership form.' % schedule_group.membership_form.content_type_map.name)
        #get UNKEYED schedule group membership forms
        # ...use the grouping key to eliminate membership forms related to a KEYED membership form from above
        qset = (
            (Q(membership_form__category__iexact=membership_form_category) |
            Q(membership_form__category__isnull=True) |
            Q(membership_form__category__exact=''))
            )
        # if 'exclude_others_if_keyed_model_name' is set it might contain the exact or part of
        # the module name. For example, subjectconsent should match subjectconsentyearzero
        # If True, add this to the filter for the list of UNKEYED membership forms
        exclude = False
        for v in keyed_membership_forms.values():
            if re.search(exclude_others_if_keyed_model_name.replace('_', ''), v._meta.object_name.lower()):
                exclude = True
        if exclude_others_if_keyed_model_name and exclude:
            qset.add(Q(membership_form__content_type_map__name__icontains=exclude_others_if_keyed_model_name), Q.AND)
        schedule_groups = super(ScheduleGroupManager, self).filter(qset)
        unkeyed_membership_forms = [schedule_group.membership_form.content_type_map
                                    for schedule_group in schedule_groups
                                        if schedule_group.grouping_key not in grouping_keys and schedule_group.membership_form.content_type_map.name not in keyed_membership_forms]
        return {'keyed': keyed_membership_forms, 'unkeyed': unkeyed_membership_forms}
