import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pyexpat.errors import messages
from typing import Optional

from fastapi import HTTPException
from httpx import Client
from sqlalchemy import false
from starlette import status

from src.apis.v1.schemas.user import UpdateUserRequest
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
        user1: Optional[User] = self.user_repo.get_user_by_email(user_data['email'])
        user2: Optional[User] = self.user_repo.get_user_by_user_name(user_data['username'])
        user3: Optional[User] = self.user_repo.get_user_by_mobile_number(user_data['mobile_number'])

        if user1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        if user2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )
        if user3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this mobile number already exists"
            )
        user_data['password'] = hash_password(user_data['password'])
        user= self.user_repo.create_user(user_data)
        if user_data['language'] == "English":
             msg = MIMEText(
                f"Hello dear user\nThank you for registering in the Finding Charger Location app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nFinding Charger Location app Support Team")
             self.send_email(user, msg)
        if user_data['language'] == "Farsi":
            msg = MIMEText(f"سلام کاربر عزیز"
                           f"\n"
                           f"از ثبت نام شما در برنامه یافتن محل شارژر متشکریم"
                           f"\n"
                           f"برای تایید حساب کاربری خود در برنامه، لطفاً از کد تایید زیر استفاده کنید:"
                           f"\n"
                           f"کد تایید:{user.email_verification_code}"
                           f"\n"
                           f"این کد فقط برای یک بار استفاده معتبر است"
                           f"\n"
                           f"با احترام،"
                           f"\n"
                           f"تیم پشتیبانی برنامه یافتن محل شارژر")
            self.send_email(user, msg)
        return user

    def login_user(self, email, password):
        user: User = self.user_repo.get_user_by_email(email)
        if user and check_password(password, user.password):
            return user
        return None

    def validate_user(self,email_verification_code:str, phone_verification_code:str, user_id: int):
        return self.user_repo.validate_user(email_verification_code, phone_verification_code, user_id)

    def resend_verification(self,user_id: int, language: str):
        user: User = self.user_repo.get_user_by_id(user_id)
        user= self.user_repo.reset_password(user.email)
        if user:
             if language == "English":
                msg = MIMEText(
                    f"Hello dear user\nThank you for registering in the Finding Charger Location app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nFinding Charger Location app Support Team")
                self.send_email(user, msg)
             if language == "Farsi":
                msg = MIMEText(f"سلام کاربر عزیز"
                               f"\n"
                               f"از ثبت نام شما در برنامه یافتن محل شارژر متشکریم"
                               f"\n"
                               f"برای تایید حساب کاربری خود در برنامه، لطفاً از کد تایید زیر استفاده کنید:"
                               f"\n"
                               f"کد تایید:{user.email_verification_code}"
                               f"\n"
                               f"این کد فقط برای یک بار استفاده معتبر است"
                               f"\n"
                               f"با احترام،"
                               f"\n"
                               f"تیم پشتیبانی برنامه یافتن محل شارژر")
                self.send_email(user, msg)
        return user

    def forgot_password(self, email_address: str, language: str) -> str:
        user= self.user_repo.reset_password(email_address)
        if user:
             if language == "English":
               msg = MIMEText(
                   f"Hello dear user\nThank you for registering in the Finding Charger Location app\nThe following verification code has been sent to you due to a forgotten password. Please use this code in the app to reset your password:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nFinding Charger Location app Support Team")
               self.send_email(user, msg)
             if language == "Farsi":
                msg = MIMEText(f"سلام کاربر عزیز"
                               f"\n"
                               f"از ثبت نام شما در برنامه یافتن محل شارژر متشکریم"
                               f"\n"
                               f"به دلیل فراموشی رمز عبور کد تایید زیر برای شما ارسال شده است، لطفاً از این کد در برنامه برای تنظیم مجدد رمز عبور استفاده کنید::"
                               f"\n"
                               f"کد تایید:{user.email_verification_code}"
                               f"\n"
                               f"این کد فقط برای یک بار استفاده معتبر است"
                               f"\n"
                               f"با احترام،"
                               f"\n"
                               f"تیم پشتیبانی برنامه یافتن محل شارژر")
                self.send_email(user, msg)
        return user

    def update_user(self,user_data: UpdateUserRequest, user_id: int):
        ## hash the password if it is provided
        if user_data.password:
            user_data.password = hash_password(user_data.password)
        else:
            user_data.password = None
        return self.user_repo.update_user(user_id, user_data)

    def send_email(self, user: User, message:str):
        msg = message
        msg["Subject"] = "email verification code"
        msg["From"] = settings.EMAIL
        msg["To"] = user.email
        try:
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL, settings.PASSWORD)
                server.sendmail(settings.EMAIL, user.email, msg.as_string())

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