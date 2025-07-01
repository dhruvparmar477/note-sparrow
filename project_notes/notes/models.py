from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import date
from django.utils.timezone import now

class Profile(models.Model):
    contact = models.BigIntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        db_table = 'profile'

class Feedback(models.Model):
    rating = models.CharField(max_length=10)
    comment = models.TextField  ()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        db_table = 'feedback'


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes'


class SentNote(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notes")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notes")
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.note.title}"
