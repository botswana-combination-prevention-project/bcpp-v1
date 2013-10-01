from __future__ import print_function
import settings
f = open('get_subtrees.sh','w')
for app in settings.INSTALLED_APPS:
    if not app.startswith('django') and app not in ['south', 'dajax', 'dajaxice', 'autocomplete']:
        print('git subtree add --prefix {0} --squash git@192.168.1.50:{0} master'.format(app), file=f)
