from itsdangerous import URLSafeTimedSerializer
from django.conf import settings




class PasswordResetTokenGenerator:
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

    def generate_token(self, user):
        return self.serializer.dumps(user.id)

    def validate_token(self, token):
        try:
            user_id = self.serializer.loads(token , max_age=120)  
            return user_id
        except Exception as e:
            return None

password_reset_token_generator = PasswordResetTokenGenerator()
             
