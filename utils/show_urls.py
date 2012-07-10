#from django.core import urlresolvers
#from django.http import HttpResponse

intro_text="""Named URL patterns for the {% url %} tag
========================================

e.g. {% url pattern-name %}
or   {% url pattern-name arg1 %} if the pattern requires arguments

"""

class ShowUrls(object):
    
    def show_url_patterns(self,):
        patterns = self._get_named_patterns()
        #r = HttpResponse(intro_text, content_type = 'text/plain')
        longest = max([len(pair[0]) for pair in patterns])
        for key, value in patterns:
            print '%s %s\n' % (key.ljust(longest + 1), value)
            print '\n'
        #return r
    
    def _get_named_patterns(self):
        "Returns list of (pattern-name, pattern) tuples"
        from django.core import urlresolvers
        resolver = urlresolvers.get_resolver(None)
        patterns = sorted([
            (key, value[0][0][0])
            for key, value in resolver.reverse_dict.items()
            if isinstance(key, basestring)
        ])
        return patterns