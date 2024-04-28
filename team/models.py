from django.db import models

# Create your models here.
class team(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=400)
    job_title = models.CharField(max_length=400)
    fb_link = models.URLField(max_length=400)
    twitter_link = models.URLField(max_length=400)
    g_scholar_link = models.URLField(max_length=400)


