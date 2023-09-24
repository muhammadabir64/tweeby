from django.db import models
from django.template.defaultfilters import truncatechars
from account.models import Account


class Tweet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name="tweet_likes", blank=True)
    comments = models.ManyToManyField("Comment", related_name="tweet_comments", blank=True)

    def total_likes(self):
        return self.likes.count()
        
    def add_like(self, user):
        self.likes.add(user)
        self.save()

    def remove_like(self, user):
        self.likes.remove(user)
        self.save()
    
    def total_comments(self):
        return self.comments.count()

    def add_comment(self, comment):
        self.comments.add(comment)
        self.save()
    
    def remove_comment(self, comment):
        self.comments.remove(comment)
        self.save()

    def __str__(self):
        return truncatechars(self.content, 25)


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content