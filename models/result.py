from django.db import models
from django.core.urlresolvers import reverse

from lab_result.models import BaseResult
from order import Order
from review import Review


class Result(BaseResult):
    """Stores result information in a one-to-many relation with :class:`ResultItem`."""
    order = models.ForeignKey(Order)
    review = models.OneToOneField(Review, null=True)
    reviewed = models.BooleanField(default=False)
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.order.aliquot.receive.registered_subject.subject_identifier
        if not self.review:
            self.review = Review.objects.create(title='{0} for {1}'.format(self.result_identifier, self.order.aliquot.receive.registered_subject.subject_identifier))
        super(Result, self).save(*args, **kwargs)

    def panel(self):
        return unicode(self.order.panel.edc_name)

    def received(self):
        return '<a href="{0}">{1}</a>'.format(self.order.aliquot.receive.get_absolute_url(), self.order.aliquot.receive)
    received.allow_tags = True

    def review_status(self):
        retval = False
        if self.review:
            if self.review.review_status == 'REVIEWED':
                retval = True
        return retval

    def report(self):
        url = reverse('view_result_report', kwargs={'section_name': 'specimens', 'result_identifier': self.result_identifier})
        url_review = reverse('admin:lab_clinic_api_review_add')
        two = ''
        if self.review:
            label = 'comment'
            url_review = self.review.get_absolute_url()
            two = """<a href="{url}" class="add-another" id="add_id_review" onclick="return showAddAnotherPopup(this);"> {label}</a>""".format(url=url_review, label=label)
        one = """<a href="{url}" class="add-another" id="add_id_report" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View report"/></a>""".format(url=url)
        return '{one}&nbsp;{two}'.format(one=one, two=two)
    report.allow_tags = True

    def ordered(self):
        return '<a href="{0}">{1}</a>'.format(self.order.get_absolute_url(), self.order)
    ordered.allow_tags = True

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['result_identifier']
