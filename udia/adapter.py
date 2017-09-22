from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from urllib.parse import urljoin

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    HACK: manually add in client URLs for valid authentication emails
    also this only works for 'activation links' and not password reset?
    """
    def send_mail(self, template_prefix, email, context):
        verify_stub = "{}/{}".format("/auth/verify-email", context["key"])
        context['activate_url'] = urljoin(settings.CLIENT_URL, verify_stub)
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
