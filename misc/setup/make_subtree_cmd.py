from __future__ import print_function
import settings
f = open('subtree_pull_all.sh','w')
for app in settings.INSTALLED_APPS:
    if not app.startswith('django') and app not in ['south', 'dajax', 'dajaxice', 'autocomplete', 'djcelery', 'databrowse']:
        print('git subtree pull -P {app} git@gitserver:{app} master'.format(app=app), file=f)

f = open('subtree_push_all.sh','w')
for app in settings.INSTALLED_APPS:
    if not app.startswith('django') and app not in ['south', 'dajax', 'dajaxice', 'autocomplete', 'djcelery', 'databrowse']:
        print('git subtree push -P {app} git@gitserver:{app} master'.format(app=app), file=f)

