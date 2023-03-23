from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    VENDOR = ('vendor', 'Vendor')
    RETAILER = ('retailer', 'Retailer')
    BUYER = ('buyer', 'Buyer')

    CATEGORY_CHOICES = (
        VENDOR,
        RETAILER,
        BUYER,
    )

    profile_pic = models.ImageField(upload_to='profile_pic', default='default_profile_pic.jpg')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=BUYER[0])
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.username}'