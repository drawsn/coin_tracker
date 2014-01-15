"""
sets the browser urls to the django admin interface and the balance_manager app
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

# the balance_manager app uses an own namespace
urlpatterns = patterns('',
    url(r'^balance_manager/', include('balance_manager.urls', namespace="balance_manager")),
    url(r'^admin/', include(admin.site.urls)),
)