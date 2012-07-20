import os
import subprocess
import tempfile
from string import Template
from lab_barcode.models import ZplTemplate, LabelPrinter, Client


class Label(object):

    """Prepares and prints a label based on a template"""

    def __init__(self, **kwargs):

        self.message = ''
        self.printer_error = False
        self.file_name = None
        self.zpl_template = None
        self.label = None
        self.label_printer = None
        self.item_count = 1
        self.item_count_total = 1
        self.client = None
        self.label_options = None

    def prepare_label_options(self, **kwargs):
        """ May be subclassed to set label dictionary """
        self.cups_server_ip = kwargs.get('cups_server_ip', None)
        self.client_ip = kwargs.get('client_ip', None)
        self.remote_addr = kwargs.get('remote_addr', None)
        self.set_template(**kwargs)
        self.set_client()
        self.label_options = kwargs

    def set_template(self, **kwargs):
        template_name = kwargs.get("template_name", None)
        template = kwargs.get("template", None)
        # use either the template name or the template instance
        if template_name:
            zpl_templates = ZplTemplate.objects.filter(name=template_name)
            if zpl_templates:
                self.zpl_template = zpl_templates[0]
            else:
                raise ValueError('Barcode ZPL template \'%s\' does not exist. ' % template_name)
        elif template:
            if isinstance(template, ZplTemplate):
                self.zpl_template = template
            else:
                raise ValueError('Parameter template must be an instance of Barcode ZplTemplate')
        else:
            # got neither template name nor a template objects but,
            # maybe one of the templates is flagged as default
            try:
                self.zpl_template = ZplTemplate.objects.get(default=True)
            except:
                # ... guess not
                raise ValueError('No valid template or template_name specified and a default '
                                 'template does not exist. Cannot continue.')

    def format_label(self):
        """ format label given a dictionary of key/value pairs prepared in a sublcass of label"""
        # convert old templates
        self.zpl_template.template = self.zpl_template.template.replace('%(', '${').replace(')s', '}')
        self.zpl_template.save()
        # safe_substitue
        self.formatted_label = self.zpl_template.template
        self.formatted_label = Template(self.zpl_template.template)
        self.formatted_label = self.formatted_label.safe_substitute(self.label_options)

    def label_to_file(self):

        """ write the label to a text file to be sent directly to the printer """
        # create temp file
        tup = tempfile.mkstemp()
        self.file_name = tup[1]
        try:
            my_file = os.fdopen(tup[0], "w")
            my_file.write(self.formatted_label)
            my_file.close()
        except:
            self.message = 'Cannot print label. Unable to create/open temporary file %s.' % self.file_name
            self.file_name = None

    def set_client(self):

        self.client = None
        client = Client.objects.filter(ip=self.client_ip)
        if client:
            self.client = client[0]

    def set_label_printer(self):

        if self.cups_server_ip:
            self.label_printer = LabelPrinter.objects.get(cups_server_ip=self.cups_server_ip)
        else:
            if self.remote_addr:
                self.label_printer = LabelPrinter.objects.get(client__ip=self.remote_addr)
                self.cups_server_ip = self.label_printer.cups_server_ip
            else:
                # TODO ask cups for default printer
                self.label_printer = None
                if self.client:
                    self.label_printer = self.client.label_printer
                else:
                    if LabelPrinter.objects.filter(default=True):
                        self.label_printer = LabelPrinter.objects.filter(default=True)[0]

    def print_label(self):

        # TODO : handle printing in windows
        self.format_label()
        if not self.formatted_label:
            raise ValueError('Cannot print label. Label has not been defined.')
        else:
            self.label_to_file()
            if self.file_name:
                # get printer
                self.set_label_printer()
                if not self.label_printer:
                    self.message = ('Cannot print label. No printers found for print '
                                   'server \'{0}\''.format(self.cups_server_ip))
                    self.printer_error = True
                else:
                    try:
                        # note -r will delete the file after printing ...
                        # TODO(erikvw): can i trap an erorr here if lpr for example does not have
                        # the -H parameter
                        subprocess.call(['lpr', '-P', self.label_printer.cups_printer_name, '-l',
                                         self.file_name, '-H', self.label_printer.cups_server_ip],
                                        shell=False)
                        self.message = 'Label sent to printer {0}'.format(self.label_printer.cups_printer_name)
                        self.printer_error = False
                    except subprocess.CalledProcessError, e:
                        self.message = ('Printer error. Unable to print test label. '
                                        'Check the printer is defined in LabelPrinter '
                                        'and ready. {0}'.format(e.output))
                        self.printer_error = True

