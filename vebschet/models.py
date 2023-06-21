from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    field = models.IntegerField(null=True, blank=True)
    counter = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'vebschet'

    def __str__(self):
        return self.user.username


class MeterReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reading = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    counter = models.ForeignKey('vebschet.UserProfile', null=True, blank=True, on_delete=models.SET_NULL)
    howireceive = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} reading'

    def save(self, *args, **kwargs):
        self.howireceive = "add from the system"
        super().save(*args, **kwargs)






