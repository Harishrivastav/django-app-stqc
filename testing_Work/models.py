from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class TestingJob(models.Model):

    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Testing','Testing'),
        ('Completed','Completed'),
    ]
    

    SRF = models.CharField(max_length=100)

    job_no = models.CharField(max_length=100)

    received_date = models.DateField()

    job_details = models.TextField()

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    progress = models.TextField(blank=True)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    report_issue_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    report_file = models.FileField(
    upload_to='reports/',
    null=True,
    blank=True
    )
    
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.job_no} - {self.assigned_to.username}"


    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=TestingJob)
def notify_engineer(sender, instance, created, **kwargs):

    if created:

        send_mail(
            'New Testing Job Assigned',
            f'You have been assigned Job No: {instance.job_no}',
            'admin@stqc.gov.in',
            [instance.assigned_to.email],
            fail_silently=False,
        )
    
class ActivityLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"