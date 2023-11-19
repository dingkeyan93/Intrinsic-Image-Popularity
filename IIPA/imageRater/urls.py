from django.urls import path

from . import views

urlpatterns = [
    path("ratings/", views.rate_image, name="rater"),
    path("ratings/<str:ratingId>", views.post_rate , name="post-rate")
]