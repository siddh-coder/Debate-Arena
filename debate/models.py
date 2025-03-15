from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Debate(models.Model):
    DEBATE_TYPES = (
        ('open', 'Open'),
        ('private', 'Private'),
    )
    topic = models.CharField(max_length=255)
    debate_type = models.CharField(max_length=7, choices=DEBATE_TYPES, default='open')
    time_limit = models.PositiveIntegerField(help_text="Time limit per participant in seconds")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_debates')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        # Only store if host is authenticated
        if not self.code:
            import random, string
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if self.host.is_authenticated:
            super().save(*args, **kwargs)
    code = models.CharField(max_length=6, unique=True, blank=True)  # For guest access, added here

    def save(self, *args, **kwargs):
        if not self.code:
            import random, string
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if self.host.is_authenticated:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic} ({self.debate_type})"

class Participant(models.Model):
    STANCES = (
        ('for', 'For'),
        ('against', 'Against'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name='participants')
    guest_name = models.CharField(max_length=50, null=True, blank=True)
    total_score = models.FloatField(default=0.0)
    stance = models.CharField(max_length=7, choices=STANCES, default='for')

    def __str__(self):
        return self.guest_name if self.user is None else self.user.username
        
class Argument(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='arguments')
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)  # AI-assigned score

    def __str__(self):
        return f"Argument by {self.participant} at {self.submitted_at}"
