from __future__ import print_function
import settings
f = open('gitrees.sample','w')
for app in settings.INSTALLED_APPS:
    if not app.startswith('django') and app not in ['south', 'dajax', 'dajaxice', 'autocomplete', 'djcelery', 'databrowse']:
        print('[subtree "{0}"]\n    url = git@gitserver:{0}\n    path =  {0}\n    branch = master\n\n'.format(app), file=f)
