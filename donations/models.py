from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):

    CATEGORY_CHOICES=[
        ('Clothes','Clothes'),
        ('Books','Books'),
        ('Toys','Toys'),
        ('Furniture','Furniture'),
        ('Household Items','Household Items'),
        ('Others','Others'),
    ]


    CONDITION_CHOICES=[
        ('New','New'),
        ('Good','Good'),
        ('Used','Used'),
    ]

    STATUS_CHOICES=[
        ('Available','Available'),
        ('donated','donated'),
    ]

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donations'
    )

    title = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()
    image=models.ImageField(
        upload_to='donations/',
        blank=True,
        null=True
    )

    condition = models.CharField(
        max_length=10,
        choices = CONDITION_CHOICES
    )

    location = models.CharField(max_length=150)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Available'

    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.title

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Donor', 'Donor'),
        ('Recipient', 'Recipient'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class DonationRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donation_requests'
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    