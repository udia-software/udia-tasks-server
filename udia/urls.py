from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import api.urls
from .views import index, null_view

# Examples:
# url(r'^$', 'udia.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    # HACK: this does not use SITE_ID, this is 'overridden' by udia.adapter
    url(r'^auth/reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        null_view,
        name='password_reset_confirm'),
    # HACK: this uses SITE_ID=1 value for domain, set info to match client site
    url(r'^auth/verify-email/(?P<key>.+)/$',
        null_view,
        name='account_confirm_email'),
]
