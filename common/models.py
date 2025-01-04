from django.db import models
import cuid

def generate_cuid():
    return cuid.cuid()

class BaseModel(models.Model):
    id = models.CharField(
        primary_key=True,
        default=generate_cuid,
        editable=False,
        max_length=25
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 