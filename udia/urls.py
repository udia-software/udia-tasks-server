from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import api.urls
import hello.views
from api.views import null_view

# Examples:
# url(r'^$', 'udia.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    # HACK: set SITE_ID=1 value for domain to be client site in model
    url(r'^auth/reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        null_view,
        name='password_reset_confirm'),
]
