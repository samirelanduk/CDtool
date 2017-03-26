from django.conf.urls import url
from cdprocessing import views

urlpatterns = [
 url(r"^$", views.single_run, name="single_run")
]
