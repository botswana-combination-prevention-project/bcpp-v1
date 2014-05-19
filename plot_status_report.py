print "******************"
print "* 75 percent data *"
print "******************"
import csv
plots_75_list = open('Otse_75pct.csv', 'r')
lines_75 = plots_75_list.readlines()
lines_75.pop(0)
plot_identifiers_75 = []
action_confirmed_75 = 0
action_unconfirmed_75 = 0
new_added_plots_75 = []
removed_plots_75 = []
for line in lines_75:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_75.append(plot_identifier)
current_db_plots_75 = Plot.objects.filter(selected=None)
current_db_plot_identifiers_75 = []
for plot in current_db_plots_75:
    current_db_plot_identifiers_75.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_75)) > len(set(plot_identifiers_75)):
    new_added_plots_75 = set(current_db_plot_identifiers_75) - set(plot_identifiers_75)
if len(set(current_db_plot_identifiers_75)) < len(set(plot_identifiers_75)):
    removed_plots_75 = set(plot_identifiers_75) - set(current_db_plot_identifiers_75)
plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_75)
for plot in plots:
    if plot.action == 'confirmed':
        action_confirmed_75 += 1
    elif plot.action == 'unconfirmed':
        action_unconfirmed_75 += 1
plots_20_list = open('Otse_20pct.csv', 'r')
lines_20 = plots_20_list.readlines()
lines_20.pop(0)
action_confirmed_20 = 0
action_unconfirmed_20 = 0
plot_identifiers_20 = []
new_added_plots_20 = []
removed_plots_20 = []
for line in lines_20:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_20.append(plot_identifier)
current_db_plots_20 = Plot.objects.filter(selected=1)
current_db_plot_identifiers_20 = []
for plot in current_db_plots_20:
    current_db_plot_identifiers_20.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_20)) > len(set(plot_identifiers_20)):
    new_added_plots20 = set(current_db_plot_identifiers_20) - set(plot_identifiers_20)
if len(set(current_db_plot_identifiers_20)) < len(set(plot_identifiers_20)):
    removed_plots_20 = set(plot_identifiers_20) - set(current_db_plot_identifiers_20)
plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_20)
for plot in plots:
    if plot.action == 'confirmed':
        action_confirmed_20 += 1
    elif plot.action == 'unconfirmed':
        action_unconfirmed_20 += 1
plots_5_list = open('Otse_backup.csv', 'r')
lines_5 = plots_5_list.readlines()
lines_5.pop(0)
action_confirmed_5 = 0
action_unconfirmed_5 = 0
plot_identifiers_5 = []
new_added_plots_5 = []
removed_plots_5 = []
for line in lines_5:
    line = line.split(',')
    plot_identifier = line[-4][1:-1]
    plot_identifiers_5.append(plot_identifier)
current_db_plots_5 = Plot.objects.filter(selected=2)
current_db_plot_identifiers_5 = []
for plot in current_db_plots_5:
    current_db_plot_identifiers_5.append(plot.plot_identifier)
if len(set(current_db_plot_identifiers_5)) > len(set(plot_identifiers_5)):
    new_added_plots5 = set(current_db_plot_identifiers_5) - set(plot_identifiers_5)
if len(set(current_db_plot_identifiers_5)) < len(set(plot_identifiers_5)):
    removed_plots_5 = set(plot_identifiers_5) - set(current_db_plot_identifiers_5)
plots = Plot.objects.filter(plot_identifier__in=current_db_plot_identifiers_5)
for plot in plots:
    if plot.action == 'confirmed':
        action_confirmed_5 += 1
    elif plot.action == 'unconfirmed':
        action_unconfirmed_5 += 1
selected

plot_to_be_on_5 = []
for p in current_db_plots_20:
    if p.comment:
        pass
    else:
        if p in Plot.objects.filter(plot_identifier__in=plot_identifiers_5):
            plot_to_be_on_5.append(p)

print "plot list still the same: ", len(set(current_db_plot_identifiers_5 + plot_identifiers_5)) == len(current_db_plot_identifiers_5) == len(plot_identifiers_5)
print "Total Plots for BHS 20 percent: ", len(plot_identifiers_5)
print "Total current Plots for BHS 20 percent in the db: ", len(current_db_plot_identifiers_5)
print "Total added plots: ", len(new_added_plots_5)
print "Total removed plots: ", len(removed_plots_5)
print "Total confirmed plots: ", action_confirmed_5
print "Total unconfirmed plots: ", action_unconfirmed_5
new_added_plots_75_list = list(new_added_plots_75)
p_20 = []
p_5 = []
for p in new_added_plots_75_list:
    if p in plot_identifiers_20:
        p_20.append(p)
    elif p in plot_identifiers_5:
        p_5.append(p)

        
print "**************************************************"
print "* Where do the extra plots in 75 percent belong *"
print "**************************************************"
print "Total plots in 75 belonging to 20 percent", len(p_20)
print "Total plots in 75 belonging to 5 percent", len(p_5)

p1_20 = Plot.objects.get(plot_identifier=p_20[0])
p12_5 = Plot.objects.filter(plot_identifier__in=p_5)
p1_5 = p12_5[0]
p2_5 = p12_5[1]
p1_5.selected=1
p1_5.save()
p2_5.selected=1
p2_5.save()
p1_20.selected=1
p1_20.save()

no_comment_identifiers = []
no_comment = Plot.objects.filter(comment__isnull=True, selected=1)
for p in no_comment:
    no_comment_identifiers.append(p.plot_identifier)
not_from_20 = set(no_comment_identifiers) - set(plot_identifiers_20)
print "Plot in 20 percent not that are to belong to 5 percent: ", len(not_from_20)


print "plot list still the same: ", len(set(current_db_plot_identifiers_75 + plot_identifiers_75)) == len(current_db_plot_identifiers_75) == len(plot_identifiers_75)
print "Total Plot sent to CDC: ", len(plot_identifiers_75)
print "Total current plots that shows to have been sent to CDC: ", len(current_db_plot_identifiers_75)
print "Total added plots: ", len(new_added_plots_75)
print "Total removed plots: ", len(removed_plots_75)
print "Total confirmed plots: ", action_confirmed_75
print "Total unconfirmed plots: ", action_unconfirmed_75
print "*******************"
print "* 20 percent data *"
print "*******************"

print "plot list still the same: ", len(set(current_db_plot_identifiers_20 + plot_identifiers_20)) == len(current_db_plot_identifiers_20) == len(plot_identifiers_20)
print "Total Plots for BHS 20 percent: ", len(plot_identifiers_20)
print "Total current Plots for BHS 20 percent in the db: ", len(current_db_plot_identifiers_20)
print "Total added plots: ", len(new_added_plots_20)
print "Total removed plots: ", len(removed_plots_20)
print "Total confirmed plots: ", action_confirmed_20
print "Total unconfirmed plots: ", action_unconfirmed_20
print "******************"
print "* 5 percent data *"
print "******************"