# Import Django's administration site.
from django.contrib import admin

# Import path for defining URLs.
# Import include so that we can connect the
# results application's URLs.
from django.urls import path, include

# Main URL configuration for the entire project.
urlpatterns = [
    path('admin/', admin.site.urls),

    # Send requests to our results application.
    #
    # For example:
    # /student/1/
    #
    # will be handled by results/urls.py.
    path("", include("results.urls")),
]
