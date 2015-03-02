from __future__ import print_function
import settings
f = open('push_subtrees.sh','w')
for app in settings.INSTALLED_APPS:
    if not app.startswith('django') and app not in ['south', 'dajax', 'dajaxice', 'autocomplete', 'tastypie']:
        print('git subtree push --prefix {0} --squash git@192.168.1.50:{0} master'.format(app), file=f)
