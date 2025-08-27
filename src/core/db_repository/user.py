import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from src.apis.v1.schemas.user import UpdateUserRequest
from src.core.models import User, Review, Car, ChargingLocation
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
        new_user = User(
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            password=user_data.get('password'),
            email=user_data.get('email'),
            address_of_home=user_data.get('address_of_home'),
            city_of_home=user_data.get('city_of_home'),
            postcode_of_home=user_data.get('postcode_of_home'),
            user_type=user_data.get('user_type'),
            mobile_number=user_data.get('mobile_number'),
            country = user_data.get('country')

        )
        new_user.email_verification_code = random.randint(10000, 99999)
        new_user.phone_verification_code = random.randint(10000, 99999)
        new_user.expired_time_email_verification = datetime.now() + timedelta(minutes=45)

        self.db.add(new_user)

        return new_user

    def get_user_by_email(self, email):
        user = self.db.query(User).filter(User.email == email).first()
        return user
    def get_user_by_user_name(self, username):
        user = self.db.query(User).filter(User.username == username).first()
        return user
    def get_user_by_mobile_number(self, mobilenumber):
        user = self.db.query(User).filter(User.mobile_number == mobilenumber).first()
        return user

    def validate_user(self, email_verification_code: str, phone_verification_code: str, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()
         # log all code and date
        logging.info(f"email_verification_code: {email_verification_code}, user.email_verification_code: {user.email_verification_code}, current_time: {datetime.now()}, expired_time_email_verification: {user.expired_time_email_verification}")
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
                   detail=f"cannot validated user: email_verification_code is not correct or expired"
                )

    def reset_password(self, email_address:str):
        if email_address:
            user = self.db.query(User).filter(User.email == email_address).first()
            if user:
                user.email_verification_code = random.randint(10000, 99999)
                user.is_validated_email = False
                user.expired_time_email_verification = datetime.now() + timedelta(minutes=15)
                self.db.commit()
                self.db.refresh(user)
                return user
            else:
                return None
        else:
            return None

    def update_user(self, user_id: int, user_data: UpdateUserRequest):
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
            if user_data.country:
                    query.country = user_data.country

            self.db.commit()
            return query
        else:
             raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail=f"Error updating user: {str(e)}"
             )

    def delete_user(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        user_id = user.user_id
        self.db.query(Review).filter(Review.user_id == user_id).delete()
        self.db.query(Car).filter(Car.user_id == user_id).delete()
        self.db.query(ChargingLocation).filter(ChargingLocation.user_id == user_id).delete()
        self.db.query(User).filter(User.user_id == user_id).delete()
        self.db.commit()


