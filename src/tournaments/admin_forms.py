from django.utils.translation import gettext_lazy as _
from unfold.forms import AuthenticationForm


class UkrainianAdminAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = _("Імʼя користувача")
        self.fields["password"].label = _("Пароль")

    error_messages = {
        "invalid_login": _(
            "Будь ласка, введіть правильні імʼя користувача та пароль. "
            "Зверніть увагу: обидва поля чутливі до регістру."
        ),
        "inactive": _("Цей обліковий запис неактивний."),
    }
