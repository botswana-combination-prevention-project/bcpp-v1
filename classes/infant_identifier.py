from datetime import datetime
from django.forms import ValidationError
from django.db.models import get_model
from bhp_identifier.models import SubjectIdentifier
from base_identifier import BaseSubjectIdentifier


class InfantIdentifier(BaseSubjectIdentifier):

    """ Creates an infant identifier derived from the maternal identifier, considers the number of infants
    during this registration session and their birth order and returns a dictionary {infant order: identifier}.

    Usage::
        >>> if not change:
        >>>    obj.user_created = request.user
        >>>    obj.save()
        >>>    if obj.live_infants_to_register > 0:
        >>>        #Allocate Infant Identifier
        >>>        infant_identifier = InfantIdentifier()
        >>>        for self.infant_order in range(0, obj.live_infants_to_register):
        >>>            infant_identifier.get_identifier(
        >>>                add_check_digit=False,
        >>>                is_derived=True,
        >>>                maternal_identifier=obj.maternal_visit.appointment.registered_subject.subject_identifier,
        >>>                maternal_study_site=obj.maternal_visit.appointment.registered_subject.study_site,
        >>>                user=request.user,
        >>>                birth_order=self.infant_order,
        >>>                live_infants=obj.live_infants,
        >>>                live_infants_to_register=obj.live_infants_to_register,
        >>>                subject_type='infant')
    """

    def consent_required(self):
        return False

    def get_identifier_prep(self, **kwargs):
        """Prepares to create an identifier consisting of the the maternal identifier and a
        suffix determined by the number of live infants from this delivery.

        For example:
          maternal_identifier=056-19800001-3 -> 2 live infants -> 056-19800001-3-
          """
        options = {}
        birth_order = kwargs.get('birth_order')
        live_infants = kwargs.get('live_infants')
        live_infants_to_register = kwargs.get('live_infants_to_register')
        # maternal identifier should exist in SubjectIdentifier
        maternal_identifier = kwargs.get('maternal_identifier')
        if not SubjectIdentifier.objects.filter(identifier=maternal_identifier):
            raise ValidationError('Unknown maternal_identifier {0}.'.format(maternal_identifier))
        # some checks on logic of live and live to register
        if live_infants_to_register == 0:
            raise ValidationError("Number of live_infants_to_register may not be 0!.")
        if live_infants_to_register > live_infants:
            raise ValidationError('Number of infants to register ({0}) may not exceed '
                                  'number of live infants ({1}).'.format(live_infants_to_register, live_infants))
        if birth_order > live_infants:
            raise ValidationError("Invalid birth order if number of live infants is {0}.".format(live_infants))
        options.update(
            app_name='bhp_identifier',
            models_name='derived_subject_identifier',
            maternal_identifier=kwargs.get('maternal_identifier'),
            maternal_study_site=kwargs.get('maternal_study_site'),
            user=kwargs.get('user'),
            suffix=self._get_suffix(birth_order, live_infants),
            identifier_format="{maternal_identifier}-{suffix}",
            subject_type='infant',
            live_infants=kwargs.get('live_infants'),
            live_infants_to_register=kwargs.get('live_infants_to_register'))
        return options

    def get_identifier_post(self, new_identifier, **kwargs):
        """ Updates registered subject after a new subject identifier is created."""
        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        RegisteredSubject.objects.create(
                subject_identifier=new_identifier,
                registration_datetime=datetime.now(),
                subject_type='infant',
                user_created=kwargs.get('user'),
                created=datetime.now(),
                first_name='',
                initials='',
                registration_status='registered',
                relative_identifier=kwargs.get('maternal_identifier'),
                study_site=kwargs.get('maternal_study_site'))
        return new_identifier

    def _get_suffix(self, birth_order, live_infants):
        """ Returns a suffix for the identifier."""
        suffix = self._get_base_suffix(live_infants)
        suffix += (birth_order) * 10
        return suffix

    def _register_infants(self, user, maternal_identifier, maternal_study_site, subject_type, live_infants, live_infants_to_register):

        """ Identify and Register infant(s) and associate with the mother's subject_identifier
        and study site.

        Infant identifier is the maternal identifier plus a suffix """

        RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        # get a starting suffix based on live_infants
        suffix = self._get_base_suffix(live_infants)
        identifier = []
        # loop through range of live_infants_to_register and register
        for infant_order in range(0, live_infants_to_register):
            # if more than one infant, increment suffix by 10's
            suffix += (infant_order) * 10
            # infant identifier is the maternal identifier plus a suffix
            identifier.append("{maternal_identifier}-{suffix}".format(maternal_identifier=maternal_identifier, suffix=suffix))
            # create new record in RegisteredSubject
            # Names, initials, gender and DOB are not expected to be known yet
            RegisteredSubject.objects.create(
                subject_identifier=identifier[infant_order],
                registration_datetime=datetime.now(),
                subject_type='infant',
                user_created=user,
                created=datetime.now(),
                first_name='',
                initials='',
                registration_status='registered',
                relative_identifier=maternal_identifier,
                study_site=maternal_study_site)
        if len(identifier) == 1:
            return identifier[0]
        else:
            return identifier

    def _get_base_suffix(self, live_infants):
        """ Return a two digit suffix based on the number of live infants.

        In the case of twins, triplets, ... will be incremented by 10's during registration for each subsequent infant registered.
        """

        if live_infants == 1:
            suffix = 10  # singlet 10
        elif live_infants == 2:
            suffix = 25  # twins 25,26
        elif live_infants == 3:
            suffix = 36  # triplets 36,37,38
        elif live_infants == 4:
            suffix = 47  # quadruplets 47,48,49,50
        else:
            raise TypeError('Ensure number of infants is greater than 0 and less than or equal to 4. You wrote %s' % (live_infants))
        return suffix
