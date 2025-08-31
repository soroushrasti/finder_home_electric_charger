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
import logging

# Initialize module logger
logger = logging.getLogger(__name__)


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
        logger.info("create_user called")
        try:
            logger.debug(
                "Incoming user_data overview: email=%s username=%s mobile=%s language=%s",
                user_data.get('email'),
                user_data.get('username'),
                user_data.get('mobile_number'),
                user_data.get('language'),
            )
        except Exception:
            # Defensive: never let logging cause failures
            logger.debug("Failed to log incoming user_data overview")

        if user_data.get('email') is not None and self.user_repo.get_user_by_email(user_data.get('email')):
            logger.warning("User creation blocked: email already exists: %s", user_data.get('email'))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistEmail"
            )
        if user_data.get('username') is not None and self.user_repo.get_user_by_user_name(user_data.get('username')):
            logger.warning("User creation blocked: username already exists: %s", user_data.get('username'))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistUsername"
            )
        if user_data.get('mobile_number') is not None and self.user_repo.get_user_by_mobile_number(user_data.get('mobile_number')):
            logger.warning("User creation blocked: mobile number already exists: %s", user_data.get('mobile_number'))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="userExistMobileNumber"
            )
        try:
            logger.debug("Hashing password for new user")
            user_data['password'] = hash_password(user_data['password'])
            user: User = self.user_repo.create_user(user_data)
            logger.info("User created in DB: id=%s email=%s", getattr(user, 'user_id', None), getattr(user, 'email', None))

            # Email selection based on language
            if user_data['language'] == "English":
                logger.info(
                    "Preparing English verification email for user_id=%s email=%s",
                    getattr(user, 'user_id', None), getattr(user, 'email', None)
                )
                msg = MIMEText(
                    f"Hello {user.first_name} {user.last_name}\nThank you for registering in the BridgeEnergy app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
                )
                self.send_email(user, msg)
            if user_data['language'] == "Farsi":
                logger.info(
                    "Preparing Farsi verification email for user_id=%s email=%s",
                    getattr(user, 'user_id', None), getattr(user, 'email', None)
                )
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
            logger.info("User creation flow completed successfully for user_id=%s", getattr(user, 'user_id', None))
            return self.get_user(user.user_id)
        except Exception as e:
            # Rollback transaction if anything fails
            logger.exception("User creation failed, rolling back transaction")
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
        logger.info("resend_verification called for user_id=%s language=%s", user_id, language)
        user: User = self.user_repo.get_user_by_id(user_id)
        user = self.user_repo.reset_password(user.email)
        if user:
            try:
                if language == "English":
                    logger.info("Sending English verification email (resend) to %s", user.email)
                    msg = MIMEText(
                        f"Hello {user.first_name} {user.last_name}\nThank you for registering in the BridgeEnergy app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
                    )
                    self.send_email(user, msg)
                if language == "Farsi":
                    logger.info("Sending Farsi verification email (resend) to %s", user.email)
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
            except Exception:
                logger.exception("Failed to resend verification email for user_id=%s", user_id)

        return user

    def forgot_password(self, email_address: str, language: str) -> str:
        logger.info("forgot_password called for email=%s language=%s", email_address, language)
        user = self.user_repo.reset_password(email_address)
        if user:
            try:
                if language == "English":
                    logger.info("Sending English forgot-password email to %s", user.email)
                    msg = MIMEText(
                        f"Hello {user.first_name} {user.last_name}\nThank you for registering in the BridgeEnergy app\nThe following verification code has been sent to you due to a forgotten password. Please use this code in the app to reset your password:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
                    )
                    self.send_email(user, msg)
                if language == "Farsi":
                    logger.info("Sending Farsi forgot-password email to %s", user.email)
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
            except Exception:
                logger.exception("Failed to send forgot-password email to %s", email_address)
        return user

    def update_user(self,user_data: UpdateUserRequest, user_id: int):
        ## hash the password if it is provided
        if user_data.password:
            user_data.password = hash_password(user_data.password)
        else:
            user_data.password = None
        return self.user_repo.update_user(user_id, user_data)

    def send_email(self, user: User, message: MIMEText):
        msg = message
        msg["Subject"] = "BridgeEnergy email verification code"
        msg["From"] = settings.EMAIL
        msg["To"] = user.email
        logger.info(
            "Attempting to send email: to=%s via %s:%s",
            user.email, getattr(settings, 'SMTP_SERVER', None), getattr(settings, 'SMTP_PORT', None)
        )
        try:
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                logger.debug("SMTP connection established, starting TLS")
                server.starttls()
                logger.debug("Logging into SMTP as %s", settings.EMAIL)
                server.login(settings.EMAIL, settings.PASSWORD)
                server.sendmail(settings.EMAIL, user.email, msg.as_string())
                logger.info("Email sent successfully to %s", user.email)

        except Exception as e:
            logger.exception(
                "Error sending email to %s via %s:%s",
                user.email, getattr(settings, 'SMTP_SERVER', None), getattr(settings, 'SMTP_PORT', None)
            )
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

    def delete_user(self, email: str):
        return self.user_repo.delete_user(email)
