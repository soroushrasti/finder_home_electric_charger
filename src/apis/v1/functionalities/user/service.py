import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from httpx import Client
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
        if user_data.get('email') is not None and self.user_repo.get_user_by_email(user_data.get('email')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistEmail"
            )
        if user_data.get('username') is not None and self.user_repo.get_user_by_user_name(user_data.get('username')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistUsername"
            )
        if user_data.get('mobile_number') is not None and self.user_repo.get_user_by_mobile_number(user_data.get('mobile_number')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistMobileNumber"
            )
        try:
            user_data['password'] = hash_password(user_data['password'])
            user: User= self.user_repo.create_user(user_data)
            if user_data['language'] == "English":
                 msg = MIMEText(
                    f"Hello dear user\nThank you for registering in the Finding Charger Location app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nFinding Charger Location app Support Team")
                 self.send_email(user, msg)
            if user_data['language'] == "Farsi":
                text = f"""
                <div dir="rtl" style="text-align: right;">
                سلام کاربر عزیز<br>
                از ثبت نام شما در برنامه محل یافتن شارژر متشکریم<br>
                برای تایید حساب کاربری خود در برنامه، لطفاً از کد تایید زیر استفاده کنید:<br>
               کد تایید:
               { user.email_verification_code } <br>
               این کد فقط برای یک بار استفاده معتبر است<br>
                با احترام،<br>
               تیم پشتیبانی برنامه یافتن محل شارژر<br>
               </div>
                """
                msg = MIMEText(text, 'html')
                self.send_email(user, msg)

            self.user_repo.db.commit()
            return self.get_user(user.user_id)
        except Exception as e:
            # Rollback transaction if anything fails
            self.user_repo.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User creation failed: {str(e)}"
            )

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
                 text = f"""
                                <div dir="rtl" style="text-align: right;">
                                سلام کاربر عزیز<br>
                                از ثبت نام شما در برنامه محل یافتن شارژر متشکریم<br>
                                برای تایید حساب کاربری خود در برنامه، لطفاً از کد تایید زیر استفاده کنید:<br>
                               کد تایید:
                               {user.email_verification_code} <br>
                               این کد فقط برای یک بار استفاده معتبر است<br>
                                با احترام،<br>
                               تیم پشتیبانی برنامه یافتن محل شارژر<br>
                               </div>
                                """
                 msg = MIMEText(text, 'html')
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
                 text = f"""
                                <div dir="rtl" style="text-align: right;">
                                سلام کاربر عزیز<br>
                                از ثبت نام شما در برنامه محل یافتن شارژر متشکریم<br>
                                به دلیل فراموشی رمز عبور کد تایید زیر برای شما ارسال شده است، لطفاً از این کد در برنامه برای تنظیم مجدد رمز عبور استفاده کنید:<br>
                               کد تایید:
                               {user.email_verification_code} <br>
                               این کد فقط برای یک بار استفاده معتبر است<br>
                                با احترام،<br>
                               تیم پشتیبانی برنامه یافتن محل شارژر<br>
                               </div>
                                """
                 msg = MIMEText(text, 'html')
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