import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException
from httpx import Client
from starlette import status
from src.apis.v1.schemas.user import UpdateUserRequest
from src.core.db_repository.user import UserRepository
import bcrypt
from src.config.base import settings
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
            # Commit user before attempting to send email so email failures don't roll back user creation
            self.user_repo.db.commit()
            logger.info("User committed to DB: id=%s", getattr(user, 'user_id', None))
        except Exception as e:
            logger.exception("User creation failed during DB operations, rolling back transaction")
            self.user_repo.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User creation failed: {str(e)}"
            )

        # Email selection based on language (non-fatal)
        if getattr(settings, 'EMAIL_ENABLED', True):
            try:
                if user_data['language'] == "English":
                    logger.info(
                        "Preparing English verification email for user_id=%s email=%s",
                        getattr(user, 'user_id', None), getattr(user, 'email', None)
                    )
                    msg = MIMEText(
                        f"Hello {user.first_name} {user.last_name if user.last_name else ''}\nThank you for registering in the BridgeEnergy app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
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
            except Exception as e:
                logger.exception("Non-fatal: failed to send verification email for user_id=%s", getattr(user, 'user_id', None))
                # Optionally enforce strict mode
                if getattr(settings, 'EMAIL_STRICT', False):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User created but email failed: {str(e)}"
                    )
        else:
            logger.info("EMAIL_ENABLED is False; skipping sending verification email")

        logger.info("User creation flow completed successfully for user_id=%s", getattr(user, 'user_id', None))
        return self.get_user(user.user_id)

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
                        f"Hello {user.first_name} {user.last_name if user.last_name else ''}\nThank you for registering in the BridgeEnergy app\nTo verify your account in the app, please use the following verification code:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
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
                        f"Hello {user.first_name} {user.last_name if user.last_name else ''}\nThank you for registering in the BridgeEnergy app\nThe following verification code has been sent to you due to a forgotten password. Please use this code in the app to reset your password:\nVerification code:{user.email_verification_code}\nThis code is valid for one-time use only\nRegards,\nBridgeEnergy app Support Team"
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

    def _send_email_postmark(self, to_email: str, subject: str, content: str, content_type: str = "text/plain"):
        logger.info("Sending email via Postmark to=%s", to_email)
        token = getattr(settings, 'POSTMARK_SERVER_TOKEN', '')
        sender = getattr(settings, 'POSTMARK_SENDER', '')
        stream = getattr(settings, 'POSTMARK_MESSAGE_STREAM', 'outbound')
        if not token or not sender:
            logger.error("Postmark config missing: POSTMARK_SERVER_TOKEN or POSTMARK_SENDER")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Email service not configured")

        url = "https://api.postmarkapp.com/email"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": token,
        }
        payload = {
            "From": sender,
            "To": to_email,
            "Subject": subject,
            "MessageStream": stream,
        }
        if content_type == "text/html":
            payload["HtmlBody"] = content
        else:
            payload["TextBody"] = content

        try:
            with Client(timeout=10.0) as client:
                resp = client.post(url, headers=headers, json=payload)
            logger.info("Postmark response: status=%s", resp.status_code)
            if 200 <= resp.status_code < 300:
                return
            # Parse error body (may include ErrorCode)
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            # If account pending approval (ErrorCode 412), suppress in non-strict mode
            if (
                not getattr(settings, 'EMAIL_STRICT', False)
                and isinstance(detail, dict)
                and detail.get('ErrorCode') == 412
            ):
                logger.warning("Postmark pending approval (ErrorCode 412). Suppressing email error in non-strict mode. detail=%s", detail)
                return
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error sending email: {detail}")
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Postmark send exception")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error sending email: {str(e)}")

    def send_email(self, user: User, message: MIMEText):
        # Branch by provider
        provider = str(getattr(settings, 'EMAIL_PROVIDER', 'smtp')).lower()
        subject = "BridgeEnergy email verification code"
        # Extract body and type from MIMEText
        subtype = message.get_content_subtype()  # 'plain' or 'html'
        try:
            body_bytes = message.get_payload(decode=True)
            body = body_bytes.decode('utf-8') if isinstance(body_bytes, (bytes, bytearray)) else (body_bytes or "")
        except Exception:
            body = message.get_payload() or ""
        content_type = "text/html" if subtype == 'html' else "text/plain"

        if provider == 'postmark':
            self._send_email_postmark(user.email, subject, body, content_type)
            return

        # Default SMTP path
        msg = message
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL
        msg["To"] = user.email
        # Resolve SMTP host for better diagnostics
        try:
            import socket
            addrs = socket.getaddrinfo(settings.SMTP_SERVER, None)
            ips = sorted({a[4][0] for a in addrs})
            logger.debug("SMTP DNS resolution: %s -> %s", settings.SMTP_SERVER, ips)
        except Exception:
            logger.exception("Failed to resolve SMTP host: %s", getattr(settings, 'SMTP_SERVER', None))
        port = int(getattr(settings, 'SMTP_PORT', 587))
        logger.info(
            "Attempting to send email: to=%s via %s:%s",
            user.email, getattr(settings, 'SMTP_SERVER', None), port
        )
        try:
            with smtplib.SMTP(settings.SMTP_SERVER, port, timeout=10) as server:
                logger.debug("SMTP connection established, starting TLS")
                server.starttls()
                logger.debug("Logging into SMTP as %s", settings.EMAIL)
                server.login(settings.EMAIL, settings.PASSWORD)
                server.sendmail(settings.EMAIL, user.email, msg.as_string())
                logger.info("Email sent successfully to %s", user.email)

        except Exception as e:
            logger.exception(
                "Error sending email to %s via %s:%s",
                user.email, getattr(settings, 'SMTP_SERVER', None), port
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
