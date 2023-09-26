from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomModelBackend(ModelBackend):
    def get_user(self, user_id):
        """
        Retrieve the user's model by user ID.
        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username):
        """
        Retrieve the user's model by username.
        """
        User = get_user_model()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate the user based on username and password.
        """
        User = get_user_model()
        user = self.get_user_by_username(username)
        if user and user.check_password(password):
            return user

    def get_user_permissions(self, user_obj, obj=None):
        """
        Retrieve user permissions.
        """
        return user_obj.user_permissions.all()

    def get_group_permissions(self, user_obj, obj=None):
        """
        Retrieve group permissions.
        """
        return user_obj.group_permissions.all()

    def get_all_permissions(self, user_obj, obj=None):
        """
        Retrieve all permissions.
        """
        return user_obj.get_all_permissions(obj=obj)

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if the user has a specific permission.
        """
        return user_obj.has_perm(perm, obj=obj)
