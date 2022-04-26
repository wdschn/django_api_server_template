from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomAuthorization(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # if reg_mobile(username):
            #     user = UserModel.objects.get(username=username)
            # elif reg_email(username):
            #     user = UserModel.objects.get(email=username)
            # else:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
