from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from urllib.parse import urljoin

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Manually set `activate_url` to point to client URL for email validation
    """
    def send_mail(self, template_prefix, email, context):
        verify_stub = "{}/{}".format("/auth/verify-email", context["key"])
        context['activate_url'] = urljoin(settings.CLIENT_URL, verify_stub)
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
