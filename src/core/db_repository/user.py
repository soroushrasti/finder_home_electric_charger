from datetime import datetime, timedelta
from email.mime.text import MIMEText
from src.core.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from starlette import status
from cmath import e
import random

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
        new_user.expired_time_email_verification = datetime.now() + timedelta(minutes=15)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def get_user_by_email(self, email):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def validate_user(self, email_verification_code: str, phone_verification_code: str, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if email_verification_code and user.email_verification_code and user.email_verification_code == email_verification_code and (user.expired_time_email_verification >= datetime.now()):
              user.is_validated_email = True
              self.db.commit()
              self.db.refresh(user)
              return user
        if phone_verification_code and user.phone_verification_code and user.phone_verification_code == phone_verification_code and (user.expired_time_phone_verification >= datetime.now()):
              user.is_validated_phone_number = True
              self.db.commit()
              self.db.refresh(user)
              return user
        else:
               raise HTTPException(
                   status_code=status.HTTP_401_UNAUTHORIZED,
                   detail=f"cannot validated user: {str(e)}"
                )

    def forgot_password(self, email_address:str):
        if email_address:
            user = self.db.query(User).filter(User.email == email_address).first()
            if user:
                user.email_verification_code = random.randint(10000, 99999)
                user.is_validated_email = False
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                return user
            else:
                return None
        else:
            return None

    def update_user(self, user_id: int, user_data):
        query = self.db.query(User).filter(User.user_id == user_id).first()
        if query:
            if user_data.username:
                query.username = user_data.username
            if user_data.first_name:
                    query.first_name = user_data.first_name
            if user_data.password:
                    query.password = user_data.password
            if user_data.last_name:
                    query.last_name = user_data.last_name
            if user_data.email:
                    query.email = user_data.email
            if user_data.address_of_home:
                    query.address_of_home = user_data.address_of_home
            if user_data.city_of_home:
                    query.city_of_home = user_data.city_of_home
            if user_data.postcode_of_home:
                    query.postcode_of_home = user_data.postcode_of_home
            if user_data.user_type:
                    query.user_type = user_data.user_type
            if user_data.mobile_number:
                    query.mobile_number = user_data.mobile_number
            if user_data.is_validated_email:
                    query.is_validated_email = user_data.is_validated_email
            if user_data.is_validated_phone_number:
                    query.is_validated_phone_number = user_data.is_validated_phone_number

            self.db.commit()
            return query
        else:
             raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error updating user: {str(e)}"
             )

