from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Barlery Administration" # Text for the main header
admin.site.site_title = "Admin Console"         # Text for the HTML title tag
admin.site.index_title = "Welcome to the Barlery Admin Console" # Text for the admin index page title

urlpatterns = [
    path("", include("barlery.urls")),
    # 'registration' URLs:
    path("accounts/", include("django.contrib.auth.urls")), # see comments below for included URLs
    path('admin/', admin.site.urls),
]

# URLs included with > path("accounts/", include("django.contrib.auth.urls")),]
#  accounts/login/ [name='login']
#  accounts/logout/ [name='logout']
#  accounts/password_change/ [name='password_change']
#  accounts/password_change/done/ [name='password_change_done']
#  accounts/password_reset/ [name='password_reset']
#  accounts/password_reset/done/ [name='password_reset_done']
#  accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
#  accounts/reset/done/ [name='password_reset_complete']