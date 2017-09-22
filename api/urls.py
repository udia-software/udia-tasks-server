from django.conf.urls import include, url
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, null_view

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'auth/', include('rest_auth.urls')),
    url(r'auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/registration/account-email-verification-sent/',
        null_view,
        name='account_email_verification_sent'),
    url(r'^auth/registration/account-confirm-email/',
        null_view,
        name='account_confirm_email'),
    url(r'^auth/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        null_view,
        name='password_reset_confirm'),
]
