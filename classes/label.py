import os, sys, subprocess, platform, tempfile
from bhp_common.utils import get_ip_address, get_iface_list
from lab_barcode.models import ZplTemplate, LabelPrinter, Client

class Label(object):

    """Prepare and print a label based on a template"""

    def __init__(self, **kwargs):
    
        self.message = ''
        self.printer_error = False         
        self.file_name = None
        self.zpl_template = None
        self.label = None
        self.label_printer = None
        self.item_count = 1
        self.item_count_total = 1
        
        # take either the template name or the template object
        template_name = kwargs.get("template_name")
        template = kwargs.get("template")
        if template_name:
            zpl_templates = ZplTemplate.objects.filter(name=template_name)
            if zpl_templates:
                self.zpl_template = zpl_templates[0]
            else:
                raise ValueError('Template \'%s\' does not exist. ' % template_name )                                    
        elif template:
            if isinstance(template, ZplTemplate):
                self.zpl_template = template                
            else:
                raise ValueError, 'Parameter template must be an instance of ZplTemplate'    
        else:
            # got neither template name nor a template objects but, 
            # maybe one of the templates is flagged as default
            try:
                self.zpl_template = ZplTemplate.objects.get(default=True)
            except:
                # ... guess not
                raise ValueError('No valid template or template_name specified and a default template does not exist. Cannot continue.')                
                
        
        self.set_label(**kwargs)

    def set_label(self, **kwargs ):

        """ format label given a dictionary of key/value pairs"""        

        self.label = self.zpl_template.template
        #self.label.format(**kwargs) 
        # try to format
        #self.formatted_label = self.label % kwargs        
        try:
            self.formatted_label = self.label % kwargs
        except KeyError, e:
            # silently fail, label will print with placeholder which should imply that all the placeholder values were not provided
            self.formatted_label = self.label
            #elf.message = Cannot print label. with data, e           
       
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

    def set_label_printer(self):

        # TODO ask cups for default printer

        #get interfaces and then ip
        client_ips  = []
        ifaces = get_iface_list()
        for iface in [i for i in ifaces if 'eth' in i]:
            client_ips.append(get_ip_address(iface))
        
        #search table and take first hit
        for client_ip in client_ips:
            if Client.objects.filter(ip=client_ip):
                client = Client.objects.get(ip=client_ip)
                break
        
        if client:
            self.label_printer = client.label_printer
        else:
            self.label_printer = LabelPrinter.objects.filter(default=True)[0]
            
        if not self.label_printer:
            raise ValueError, 'Cannot print label. Label printer has no client with your ip address OR no default label printer defined'
        
    def print_label(self):

        # TODO : handle printing in windows
        
        if not self.label:
            raise ValueError, 'Cannot print label. Label has not been defined.'
        else:    
            self.label_to_file()
            if self.file_name:            
                # get printer
                self.set_label_printer()
                if not self.label_printer:
                    self.message = 'Cannot print label. No printers defined'  
                else:
                    #send lpr command
                    #if sys.version_info.major == 2 and sys.version_info.minor < 7:
                    subprocess.Popen(['lpr', '-P' ,self.label_printer.cups_printer_name, '-l', self.file_name, '-r'],shell=False)
                    #else:
                    #    subprocess.check_output(['lpr', '-P' ,self.label_printer.cups_printer_name, '-l', self.file_name, '-r'], shell=False)                                        
                    try:
                        # note -r will delete the file after printing ...
                        #subprocess.Popen(['lpr', '-P' ,self.label_printer.cups_printer_name, '-l', self.file_name],shell=False)
                        #raise TypeError()
                        if sys.version_info.major == 2 and sys.version_info.minor < 7:
                            subprocess.check_call(['lpr', '-P' ,self.label_printer.cups_printer_name, '-l', self.file_name, '-r'], shell=False)                                        
                        else:
                            subprocess.check_output(['lpr', '-P' ,self.label_printer.cups_printer_name, '-l', self.file_name, '-r'], shell=False)                                        
                        self.message = "Label printed successfully"
                        self.printer_error = False            
                    except subprocess.CalledProcessError, e:
                        self.message = "Printer error. Unable to print test label. Check the printer is defined in LabelPrinter and ready. %s" % e.output
                        self.printer_error = True

