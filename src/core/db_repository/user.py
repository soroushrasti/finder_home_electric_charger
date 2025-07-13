import bcrypt

from src.core.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
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
        new_user.email_verification_code = self.hash_code(random.randint(10000, 99999))
        new_user.phone_verification_code = self.hash_code(random.randint(10000, 99999))

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def get_user_by_email(self, email, password):
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def validate_user(self, email_verification_code: str, phone_verification_code: str, user_id: int):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        email_is_correct = bcrypt.checkpw(email_verification_code.encode('utf-8'), user.email_verification_code.encode('utf-8'))
        phone_is_correct = bcrypt.checkpw(phone_verification_code.encode('utf-8'), user.phone_verification_code.encode('utf-8'))

        if email_verification_code and user.email_verification_code and email_is_correct:
              user.is_validated_email = True
              self.db.commit()
              self.db.refresh(user)
              return user
        if phone_verification_code and user.phone_verification_code and phone_is_correct:
              user.is_validated_phone_number = True
              self.db.commit()
              self.db.refresh(user)
              return user
        else:
               raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail=f"Error validate user: {str(e)}"
                )


    def update_user(self, user_id: int, user_data: dict):
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

    def hash_code(self, plain_code: int) -> str:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(str(plain_code).encode('utf-8'), salt)
            return hashed.decode('utf-8')