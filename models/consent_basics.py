from django.db import models
from bhp_subject.models import BaseSubject


class ConsentBasics(BaseSubject):
    """Adds questions to confirm the consent process was followed."""

    pass

    class Meta:
        abstract = True
