from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q

UserModel = get_user_model()


class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        # user_params = {}
        # user_params = Q(email=username) | Q(phone=username)
        try:
            validate_email(username)
            is_email = True
            # user_params = {
            #     'email': username
            # }
        except ValidationError:
            is_email = False
            # user_params = {
            #     'phone': username
            # }

        try:
            # user = UserModel._default_manager.get(
            # **user_params
            # )
            user = UserModel._default_manager.get(
                Q(email=username) | Q(phone=username))
        except UserModel.DoesNotExist:

            UserModel().set_password(password)
        else:
            if user.check_password(password) \
                    and self.user_can_authenticate(user, is_email):
                return user

    def user_can_authenticate(self, user, is_email=True):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        valid = getattr(user, "is_active", True)
        if not is_email:
            valid &= getattr(user, "is_phone_valid", False)
        return getattr(user, "is_active", True)
