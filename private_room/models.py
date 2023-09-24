from django.db import models
from account.models import Account


class  Message(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="private_msg")
    text = models.TextField()
    room = models.CharField(null=True, blank=True, max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room