from django import forms


class PlotRadius(forms.Form):
    plot_identifier = forms.CharField(label='Plot identifier', required=True)
    radius = forms.DecimalField(label='plot radius (m)', required=True)

    def clean_plot_radius_form(self):
        plot_identifier = self.cleaned_data['plot_identifier']
        if plot_identifier is None:
            raise forms.ValidationError("plot_identifier is required")
        return plot_identifier
