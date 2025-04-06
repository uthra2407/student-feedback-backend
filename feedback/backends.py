# feedback/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Student, Institution

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Student.objects.get(email=username)
        except Student.DoesNotExist:
            try:
                user = Institution.objects.get(email=username)
            except Institution.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            try:
                return Institution.objects.get(pk=user_id)
            except Institution.DoesNotExist:
                return None
