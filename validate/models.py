from django.db import models
from django.utils import timezone
# Create your models here.
class validate(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(validate, self).save(*args, **kwargs)
    def __str__(self):
        return self.name