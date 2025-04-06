from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import Institution

class InstitutionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or "Bearer " not in auth_header:
            return None

        try:
            token_str = auth_header.split(' ')[1]
            decoded_token = AccessToken(token_str)
            institution_id = decoded_token.get('institution_id')

            # ✅ Correct Institution Lookup
            institution = Institution.objects.get(id=institution_id)
            return (institution, None)

        except Exception:
            raise AuthenticationFailed('Invalid token or institution not found')
