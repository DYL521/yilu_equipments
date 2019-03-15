from django.db import models


class ActiveUpdateModelCommon(models.Model):
    """abstract class for models with active and last_update fields"""
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_update = models.DateTimeField(auto_now=True, editable=False, db_index=True)
