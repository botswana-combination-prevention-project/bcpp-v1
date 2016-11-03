from __future__ import print_function
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_clinic.models import ClinicHouseholdMember, ClinicConsent, ClinicOffStudy
from edc.subject.registration.models import RegisteredSubject
from edc.subject.appointment.models import Appointment
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.device.sync.models.outgoing_transaction import OutgoingTransaction


class ClinicRegisteredSubjectHelper(object):

    def find_duplicates(self):
        duplicates = RegisteredSubject.objects.raw(
            '''SELECT *, count(identity) as duplicate_count
            from bhp_registration_registeredsubject GROUP BY identity having duplicate_count >1''')
        return duplicates

    def determine_bcpp_registered_subject(self, identity):
        clinic_plot_identifiers = ['120000-00', '140000-00', '160000-00',
                                   '180000-00', '210000-00', '270000-00',
                                   '350000-00']
        hhm = HouseholdMember.objects.filter(
            Q(registered_subject__identity='884820716'),
            ~Q(household_structure__household__plot__plot_identifier__in=clinic_plot_identifiers),
            ~Q(household_structure__household__plot__status='bcpp_clinic')
        )
        return hhm[0].registered_subject if hhm else None

    def get_all_clinic_models(self):
        clinic_models = [
            ClinicHouseholdMember, ClinicConsent, Appointment, ScheduledEntryMetaData, ClinicOffStudy
        ]
        return clinic_models

    def update_clinic_appointment(self, bcpp_registered_subject):
            mymodel = None
            try:
                mymodel = Appointment.objects.get(
                    registered_subject__identity=bcpp_registered_subject.identity,
                    visit_definition__code='C0')
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()
            except Appointment.DoesNotExist:
                pass
            except MultipleObjectsReturned:
                for mymodel in Appointment.objects.filter(
                        registered_subject__identity=bcpp_registered_subject.identity,
                        visit_definition__code='C0'):
                    mymodel.registered_subject = bcpp_registered_subject
                    mymodel.save()

    def update_clinic_appointment_audit(self, bcpp_registered_subject):
        mymodel = None
        try:
            mymodel = Appointment.history.get(
                registered_subject__identity=bcpp_registered_subject.identity,
                visit_definition__code='C0')
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except Appointment.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            for mymodel in Appointment.history.filter(
                    registered_subject__identity=bcpp_registered_subject.identity,
                    visit_definition__code='C0'):
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()

    def update_scheduledentrymetadata(self, bcpp_registered_subject):
        mymodel = None
        try:
            mymodel = ScheduledEntryMetaData.objects.get(
                registered_subject__identity=bcpp_registered_subject.identity,
                appointment__visit_definition__code='C0')
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except ScheduledEntryMetaData.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            for mymodel in ScheduledEntryMetaData.objects.filter(
                    registered_subject__identity=bcpp_registered_subject.identity,
                    appointment__visit_definition__code='C0'):
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()

    def update_clinic_household_member(self, bcpp_registered_subject):
        try:
            mymodel = ClinicHouseholdMember.objects.get(
                Q(registered_subject__identity=bcpp_registered_subject.identity),
                Q(household_structure__household__plot__status='bcpp_clinic'))
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except ClinicHouseholdMember.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            for mymodel in ClinicHouseholdMember.objects.filter(
                    Q(registered_subject__identity=bcpp_registered_subject.identity),
                    Q(household_structure__household__plot__status='bcpp_clinic')):
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()

    def update_clinic_household_member_audit(self, bcpp_registered_subject):
        try:
            mymodel = ClinicHouseholdMember.history.get(
                Q(registered_subject__identity=bcpp_registered_subject.identity),
                Q(household_structure__household__plot__status='bcpp_clinic'))
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except ClinicHouseholdMember.DoesNotExist:
            pass
        except MultipleObjectsReturned:
            for mymodel in ClinicHouseholdMember.history.filter(
                    Q(registered_subject__identity=bcpp_registered_subject.identity),
                    Q(household_structure__household__plot__status='bcpp_clinic')):
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()

    def update_clinic_off_study(self, bcpp_registered_subject):
        try:
            mymodel = ClinicOffStudy.objects.get(
                Q(registered_subject__identity=bcpp_registered_subject.identity))
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except ClinicOffStudy.DoesNotExist:
            pass

    def update_clinic_off_study_audit(self, bcpp_registered_subject):
        try:
            mymodel = ClinicOffStudy.history.get(
                Q(registered_subject__identity=bcpp_registered_subject.identity))
            mymodel.registered_subject = bcpp_registered_subject
            mymodel.save()
        except ClinicOffStudy.DoesNotExist:
            pass

    def update_clinic_consent(self, bcpp_registered_subject):
        try:
            try:
                mymodel = ClinicConsent.objects.get(
                    Q(household_member__household_structure__household__plot__status='bcpp_clinic'),
                    Q(identity=bcpp_registered_subject.identity))
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()
            except AttributeError as error:
                print ('Error {}'.format(error))
        except ClinicConsent.DoesNotExist:
            pass

    def update_clinic_consent_audit(self, bcpp_registered_subject):
        try:
            try:
                mymodel = ClinicConsent.history.get(
                    Q(household_member__household_structure__household__plot__status='bcpp_clinic'),
                    Q(identity=bcpp_registered_subject.identity))
                mymodel.registered_subject = bcpp_registered_subject
                mymodel.save()
            except AttributeError as error:
                print ('Error {}'.format(error))
        except ClinicConsent.DoesNotExist:
            pass

    def replace_registered_subject_for_clinic_models(self, bcpp_registered_subject, clinic_model):
        if clinic_model._meta.model_name == 'appointment':
            self.update_clinic_appointment(bcpp_registered_subject)
            self.update_clinic_appointment_audit(bcpp_registered_subject)
        elif clinic_model._meta.model_name == 'scheduledentrymetadata':
            self.update_scheduledentrymetadata(bcpp_registered_subject)
        elif clinic_model._meta.model_name == 'clinichouseholdmember':
            self.update_clinic_household_member(bcpp_registered_subject)
            self.update_clinic_household_member_audit(bcpp_registered_subject)
        elif clinic_model._meta.model_name == 'clinicconsent':
            self.update_clinic_consent(bcpp_registered_subject)
            self.update_clinic_consent_audit(bcpp_registered_subject)
        elif clinic_model._meta.model_name == 'clinicoffstudy':
            self.update_clinic_off_study(bcpp_registered_subject)
            self.update_clinic_off_study_audit(bcpp_registered_subject)

    def track_outgoing_transactions(self):
        transact_list = [model_name._meta.model_name for model_name in self.get_all_clinic_models()]
        out_trans = OutgoingTransaction.objects.filter(tx_name__in=transact_list)
        for transactions in out_trans:
            if transactions.modified == datetime.today():
                transactions.delete()

    def update_clinic_registered_subject(self):
        i = 1
        for subjects in self.find_duplicates():
            bcpp_registered_subject = self.determine_bcpp_registered_subject(subjects.identity)
            print ('{0}. {1}'.format(i, bcpp_registered_subject))
            i += 1
            for clinic_model in self.get_all_clinic_models():
                self.replace_registered_subject_for_clinic_models(bcpp_registered_subject, clinic_model)
                print ('{} updated'.format(clinic_model._meta.model_name))
