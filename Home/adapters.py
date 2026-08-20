from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from allauth.account.adapter import DefaultAccountAdapter


WELCOME_RETURN_URL_SESSION_KEY = "wikonomi_welcome_return_url"


class WikonomiAccountAdapter(DefaultAccountAdapter):
    """Route brand-new accounts through the Wikonomi welcome page once."""

    def post_login(
        self,
        request,
        user,
        *,
        email_verification,
        signal_kwargs,
        email,
        signup,
        redirect_url,
    ):
        # Let allauth complete its normal login work first (signals, messages,
        # and calculation of the final `next` destination).
        response = super().post_login(
            request,
            user,
            email_verification=email_verification,
            signal_kwargs=signal_kwargs,
            email=email,
            signup=signup,
            redirect_url=redirect_url,
        )

        if not signup:
            return response

        return_url = getattr(response, "url", None) or reverse("Home:home")
        allowed_hosts = {request.get_host()}

        if not url_has_allowed_host_and_scheme(
            url=return_url,
            allowed_hosts=allowed_hosts,
            require_https=request.is_secure(),
        ):
            return_url = reverse("Home:home")

        request.session[WELCOME_RETURN_URL_SESSION_KEY] = return_url
        response["Location"] = reverse("Home:welcome")
        return response
