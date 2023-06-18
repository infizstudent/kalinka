from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    plot_number = models.IntegerField(null=True, blank=True)
    counter_number = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'vebschet'

    def __str__(self):
        return self.user.username

