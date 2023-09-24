from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account.views import login_page


urlpatterns = [
    path("admin/login/", login_page),
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include("feed.urls")),
    path("", include("global_room.urls")),
    path("", include("private_room.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)