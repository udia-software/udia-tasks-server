from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import api.urls
import hello.views

# Examples:
# url(r'^$', 'udia.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
