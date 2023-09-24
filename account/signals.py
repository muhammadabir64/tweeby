from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account
import uuid

def thread_gen(length):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:length]

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(user=instance)
        account.thread_code = thread_gen(10)
        account.save()