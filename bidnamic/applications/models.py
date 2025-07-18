from django.db import models


class Application(models.Model):
    HIGH, MEDIUM, LOW = range(3)
    BIDDING_SETTING_CHOICES = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    )
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    date_of_birth = models.DateField(verbose_name="Date of birth")
    company_name = models.CharField(max_length=150)
    address = models.TextField()
    telephone = models.CharField(max_length=15)
    google_account_ads_id = models.CharField(
        verbose_name="Google Ads Account ID", max_length=200
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    bidding_setting = models.ForeignKey('applications.BiddingSetting', on_delete=models.CASCADE)

class BiddingSetting(models.Model):
    VERSION_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    )
    max_bid = models.CharField(max_length=150)
    min_bid = models.CharField(max_length=150)
    budget = models.CharField(max_length=150)
    algorithm = models.CharField(max_length=150)
    version = models.CharField(choices=VERSION_CHOICES, max_length=3)


