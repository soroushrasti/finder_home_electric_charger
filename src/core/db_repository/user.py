import smtplib
from email.mime.text import MIMEText
import random
from typing import Any

from sqlalchemy.testing.suite.test_reflection import users

from src.core.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from cmath import e


class UserRepositoryAbstract:
    def get_user_by_id(self, user_id):
        pass

    def create_user(self, user_data):
        pass

    def get_user_by_email(self, username, password):
        pass


class UserRepository(UserRepositoryAbstract):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> type[User] | None:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def create_user(self, user_data: dict) -> User:
        new_user = User(**user_data)
        new_user.email_verification_code = random.randint(10000, 99999)
        new_user.phone_verification_code = random.randint(10000, 99999)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        msg = MIMEText(f"Thanks for registration in finding charger location app. This is your verification code: {new_user.email_verification_code}")
        msg["Subject"] = "email verification code"
        msg["From"] = "<EMAIL>"
        msg["To"] = new_user.email
        try:
            with smtplib.SMTP('localhost', 465) as server:
                server.starttls()
                server.login("<EMAIL>", "password")
                server.sendmail("<EMAIL>", new_user.email, msg.as_string())

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error sending email: {str(e)}"
            )
        return new_user

    def get_user_by_email(self, email, password):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def validate_user(self, email_verification_code: str, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user.email_verification_code == email_verification_code:
              user.is_validated = True
              self.db.commit()
              self.db.refresh(user)
              return user
        else:
               raise HTTPException(
                   status_code=status.HTTP_404_BAD_REQUEST,
                   detail=f"Error validate user: {str(e)}"
                )

