from django.conf.urls import url
from cdprocessing import views

urlpatterns = [
 url(r"^single/$", views.single_run, name="single_run"),
 url(r"^$", views.home_page, name="home_page")
]
