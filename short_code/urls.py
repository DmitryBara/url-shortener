from django.urls import path
from .views import ShortCodeEndpoint, redirect_by_short_code

urlpatterns = [
    path(r'shorten/', ShortCodeEndpoint.as_view()),
    path(r'<str:short_code>/stats', ShortCodeEndpoint.as_view()),
    path(r'<str:short_code>', redirect_by_short_code),
]