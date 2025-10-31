from django.urls import path

from . import views

app_name = "mailgun"

urlpatterns = [
    path("feedback/send/", views.send_feedback, name="send_feedback"),
    path("booking/send/", views.send_booking, name="send_booking"),
]
