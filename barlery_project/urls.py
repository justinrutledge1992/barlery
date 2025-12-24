from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Barlery Administration"
admin.site.site_title = "Admin Console"
admin.site.index_title = "Welcome to the Barlery Admin Console"

urlpatterns = [
    path("", include("barlery.urls")),
    # 'registration' URLs - Using custom login/logout views from barlery.urls
    # path("accounts/", include("django.contrib.auth.urls")), # Commented out - using custom views
    path('admin/', admin.site.urls),
]