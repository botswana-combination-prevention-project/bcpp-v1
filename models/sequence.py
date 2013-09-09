from base_sequence import BaseSequence


class Sequence(BaseSequence):

    class Meta:
        app_label = "bhp_identifier"
        ordering = ['id', ]
