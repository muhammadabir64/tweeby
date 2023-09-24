from django.contrib import admin
from django.utils.html import format_html
from .models import Account


admin.site.index_title = "Tweeby"
admin.site.site_header = "Tweeby Dashboard"
admin.site.site_title = "Tweeby Dashboard"

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["id", "avatar", "user", "email", "flag_icon", "country", "thread_code", "date_joined"]
    list_display_links = ["id", "avatar", "user", "email", "flag_icon", "country", "thread_code", "date_joined"]
    list_per_page = 25
    readonly_fields = ["thread_code", "date_joined"]

    def email(self, obj):
        return obj.user.email

    def date_joined(self, obj):
        return obj.user.date_joined.strftime("%d %b %Y")

    def avatar(self, obj):
        return format_html("<img src='{}' width='25px' height='25px' style='border-radius: 50%;' />".format(obj.profile_img))
    
    def flag_icon(self, obj):
        return format_html("<img src='../../../static/flags/{}.svg' width='25px' />".format(obj.flag))