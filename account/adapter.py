from __future__ import unicode_literals

from allauth.utils import (
    import_attribute,
)
from allauth import app_settings
from allauth.account.adapter import DefaultAccountAdapter


class CustomAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_field, user_username

        data = form.cleaned_data
        username = data.get("username")
        nickname = data.get("nickname")
        is_creator = data.get("is_creator")
        channel_url = data.get("channel_url")
        channel_category = data.get("channel_category")
        channel_intro = data.get("channel_intro")
        bank = data.get("bank")
        depositor = data.get("depositor")
        account = data.get("account")
        user_username(user, username)

        if "password1" in data:
            user.set_password(data["password1"])

        if nickname:
            user_field(user, "nickname", nickname)
        if is_creator:
            user_field(user, "is_creator", is_creator)
        if channel_url:
            user_field(user, "channel_url", channel_url)
        if channel_category:
            user_field(user, "channel_category", channel_category)
        if channel_intro:
            user_field(user, "channel_intro", channel_intro)
        if bank:
            user_field(user, "bank", bank)
        if depositor:
            user_field(user, "depositor", depositor)
        if account:
            user_field(user, "account", account)

        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user


def get_adapter(request=None):
    return import_attribute(app_settings.ADAPTER)(request)
