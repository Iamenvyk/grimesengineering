from django.db import models

# from imagekit.models import ImageSpecField
# from pilkit.processors import ResizeToFit
from ga.services.models import Department
from ga.functions import upload_path, prefetch_id

class LicenseCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "License Categories"

    def __unicode__(self):
        return self.name

class LicenseName(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class License(models.Model):
    name = models.ForeignKey(to=LicenseName)
    number = models.CharField(max_length=100)
    category = models.ForeignKey(to=LicenseCategory)
    
    def __unicode__(self):
        return '%s; %s' % (self.name.name, self.number)

class Staff(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True,)
    title = models.CharField(max_length=500, null=True, blank=True,)
    license = models.ManyToManyField(License, null=True, blank=True, related_name="staff")
    description = models.TextField(null=True, blank=True,)
    phone = models.CharField(max_length=100, null=True, blank=True,)
    cell = models.CharField(max_length=100, null=True, blank=True,)
    department = models.ForeignKey(to=Department, null=True, blank=True,)
    active = models.BooleanField(default=True)
    sort = models.IntegerField(default=10, null=True,)
    image = models.ImageField(null=True, blank=True, upload_to = upload_path)
#     thumb = ImageSpecField(
#         source='image',
#         processors=[ResizeToFit(250, 250)],
#         format='JPEG',
#         options={'quality': 60},
#     )
    def save(self, *args, **kwargs):
        if not self.id and self.image:
            self.id = prefetch_id(self)
        super(Staff, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Staff"
        
    def __unicode__(self):
        return self.name