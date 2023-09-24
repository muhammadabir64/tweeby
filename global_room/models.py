from django.db import models
from account.models import Account


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text