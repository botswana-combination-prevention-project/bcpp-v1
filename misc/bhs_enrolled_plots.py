
"""All enrolled plots"""
c = SubjectConsent.objects.all()
plots = []
for j in c:
    plots.append(j.household_member.household_structure.household.plot.plot_identifier)
plots = list(set(plots))
f = open('/Users/django/Desktop/molapowabojang_enrolled_plots.txt', 'wb')
for p in plots:
    st = '\'' + str(p) + '\'' + ','
    f.write(st)
    f.write('\n')
