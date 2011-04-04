
class F0110Responsereference(models.Model):
    code = models.CharField(max_length=75, blank=True)
    name = models.CharField(max_length=765, blank=True)
    utestid_units = models.CharField(max_length=75, blank=True)
    utestid_dec = models.IntegerField(null=True, blank=True)
    lln = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    uln = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    special_comment = models.CharField(max_length=765, blank=True)
    gender = models.CharField(max_length=75, blank=True)
    age_low = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    age_low_unit = models.CharField(max_length=75, blank=True)
    age_low_quantifier = models.CharField(max_length=75, blank=True)
    age_high = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    age_high_unit = models.CharField(max_length=75, blank=True)
    age_high_quantifier = models.CharField(max_length=75, blank=True)
    panic_value = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    panic_value_quantifier = models.CharField(max_length=75, blank=True)


