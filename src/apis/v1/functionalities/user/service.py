import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from httpx import Client
from starlette import status
from src.core.db_repository.user import UserRepositoryAbstract, UserRepository
import bcrypt
from src.config.base import BaseConfig, settings
from src.core.models import User


def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    # Add to src/apis/v1/functionalities/user/service.py
    def create_user(self, user_data: dict):
        user_data['password'] = hash_password(user_data['password'])
        return self.user_repo.create_user(user_data)

    def login_user(self, email, password):
        user: User = self.user_repo.get_user_by_email(email, password)
        if user and check_password(password, user.password):
            return user
        return None

    def validate_user(self,email_verification_code:str, sms_verification_code:str, user_id: int):
        return self.user_repo.validate_user(email_verification_code, sms_verification_code, user_id)

    def update_user(self,user_data:dict, user_id: int):
        return self.user_repo.update_user(user_id, user_data)

    def send_email(self, user_data: dict):
        msg = MIMEText(
            f"Thanks for registration in finding charger location app. This is your verification code: {user_data.email_verification_code}")
        msg["Subject"] = "email verification code"
        msg["From"] = settings.EMAIL
        msg["To"] = user_data.email
        try:
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL, settings.PASSWORD)
                server.sendmail(settings.EMAIL, user_data.email, msg.as_string())

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error sending email: {str(e)}"
            )


    def send_sms(self, user_data: dict):
        client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
        try:
           client.message.create("sms body message", settings.TWILIO_NUMBER, user_data.mobile_number)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error sending sms: {str(e)}"
            )