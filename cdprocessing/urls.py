from django.conf.urls import url
from cdprocessing import views

urlpatterns = [
 url(r"^$", views.home_page, name="home_page")
]
