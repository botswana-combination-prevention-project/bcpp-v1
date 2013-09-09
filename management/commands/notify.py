from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from optparse import make_option
from django.core.mail import send_mail
from django.db.models import Count, get_model
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings



class Command(BaseCommand):
    """ Sends an email or sms notification to a list of recipients if not labs results have been
    imported into the local EDC 24 hrs
    """
    args = ('--email <email>  --sms <cellphone>')
    help = 'Manage labs_notification import.'
    option_list = BaseCommand.option_list + (
        make_option('--email',
            dest='send_email',
            action='store_true',
            default=False,
            help=('Send an email nofication.')),
         )
    option_list += (
        make_option('--sms',
            dest='send_sms',
            action='store_true',
            default=False,
            help=('Send SMS nofication.')),
        )
    
    def handle(self, *args, **options):
        count           = 0
        import_age      = 24
        email_sender    = 'django@bhp.org.bw'
        recipient_list  = []
        now             = datetime.today()
        cut_off_date    = now - relativedelta(hours = import_age)
        
        count           = self.get_import_results_count(import_age, cut_off_date)
        if count > 0:
            print "{0} results imported between {1} and {2}. No need to send notification".format(count, cut_off_date, now)
        else:
            if not args:
                args = [None]
            
            if options['send_email']:
                for recipient in args:
                    recipient_list.append(recipient)
                print "sending email to {0}".format(recipient_list)
                if len(recipient_list):
                    self.send_email(email_sender, recipient_list, import_age)
                
            elif options['send_sms']:
                for recipient in args:
                    recipient_list.append(recipient)
                    
                print "sending sms to {0}".format(recipient_list)
                if len(recipient_list):
                    self.send_sms(recipient_list, import_age)
            
            else:
                raise CommandError('Unknown option, Try --help for a list of valid options')

    def send_sms(self, recipient_list, import_age):
        pass
    def send_email(self, email_sender, recipient_list, import_age):
        subject     = "{0}: No labs have been imported in {1}hrs".format(date.today(), import_age)
        body        = "No labs have been imported from the LIS/DMIS for the past {0}. Check import_dmis and import_lis".format(import_age)
        email_sent  = send_mail(subject, body, email_sender, recipient_list, fail_silently=False)        

    def get_import_results_count(self, import_age, cut_off_date):
        Result = get_model('lab_clinic_api','Result')
        cut_off_date = datetime.now() - relativedelta(hours = import_age)
        ret_val = Result.objects.filter(import_datetime__gte=cut_off_date).count()
        return ret_val
        