import syslog
import time

class SyslogOutput:
    
    def process_exception(self, request, exception):
    
        # Compile the string for the exception in the format: "Variable: Value" so as to make it readable
        syslog.syslog('os_variables:')
        request_string = ""
        filename='/home/erikvw/django_%s_error.csv'%(time.strftime('%y-%m-%d-%H-%M-%s'))
        txt = file(filename, 'w')
        
        for item in dir(request):
            value = getattr(request, item)
            request_string += "%s:  %s\n"%(item, value)
            request_string += "\n\Exception: %s"%(exception)
        syslog(request_string)
        txt.writelines("Exception: %s"%(request_string))
        txt.close()        
        return None

