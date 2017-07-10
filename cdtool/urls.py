"""cdtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from cdcrunch.views import tool_page
import home.views as home_views

urlpatterns = [
 url(r"^changelog/$", home_views.changelog_page, name="changelog_page"),
 url(r"^help/$", home_views.help_page, name="help_page"),
 url(r"^about/$", home_views.about_page, name="about_page"),
 url(r"^$", tool_page, name="tool_page")
]
