from django.contrib import admin
from django.template.defaultfilters import truncatechars
from .models import Tweet, Comment

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "tweet", "total_likes", "total_comments", "published"]
    list_display_links = ["user", "tweet"]
    list_per_page = 25

    def tweet(self, obj):
        return truncatechars(obj.content, 25)

    def published(self, obj):
        return obj.publish_date.strftime("%d %b %Y")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "comment", "published"]
    list_display_links = ["user", "post", "comment"]
    list_per_page = 25

    def post(self, obj):
        return truncatechars(obj.tweet, 25)

    def comment(self, obj):
        return truncatechars(obj.content, 25)

    def published(self, obj):
        return obj.publish_date.strftime("%d %b %Y")