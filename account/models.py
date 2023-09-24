from django.db import models
from django.contrib.auth.models import User


profile_img_url = "https://firebasestorage.googleapis.com/v0/b/tweeby-6bcd3.appspot.com/o/default_avatar.png?alt=media&token=c7f99452-f467-4c0f-bd11-68fca7d33803"
cover_img_url = "https://firebasestorage.googleapis.com/v0/b/tweeby-6bcd3.appspot.com/o/default_cover.png?alt=media&token=544cd572-0031-4a55-822c-152907ce3a43"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.URLField(default=profile_img_url)
    cover_img = models.URLField(default=cover_img_url)
    bio = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    flag = models.CharField(max_length=25)
    country = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    star_badge = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=False)
    thread_code = models.CharField(max_length=125)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="user_followers")
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="user_following")


    def add_follower(self, user):
        self.followers.add(user)
        self.save()
    
    def remove_follower(self, user):
        self.followers.remove(user)
        self.save()
    
    def add_following(self, user):
        self.following.add(user)
        self.save()

    def remove_following(self, user):
        self.following.remove(user)
        self.save()

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()

    def __str__(self):
        return self.user.username