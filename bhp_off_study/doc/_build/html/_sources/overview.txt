Overview
========

Module :mod:`bhp_off_study` manages taking a subject off study. Data may not be collected on a date
after the date the subject is taken off study. However, existing data should be editable even after
a subject is taken off study. Additionally, an off study report should be rejected if the date subject
taken off study is before the report date of existing data.

Module :mod:`bhp_off_study` makes use of a mixin :class:`bhp_off_study.mixins.OffStudyMixin`. The mixin has 
methods that help a save method determine the study status of a subject and whether or not to allow the
data to be saved.

All local models that require consent should have access to the mixin methods since the methods are 
referred to by :mod:`bhp_consent` at the save level.

