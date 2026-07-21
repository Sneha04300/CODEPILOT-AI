from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token


class AuthService:

    @staticmethod
    def register(user_data: UserRegister, db: Session):

        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(user_data.password)

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token(
            {
                "sub": str(new_user.id),
                "email": new_user.email,
            }
        )

        return {
            "message": "User registered successfully",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(new_user.id),
                "full_name": new_user.full_name,
                "email": new_user.email,
            },
        }

    @staticmethod
    def login_user(user_data: UserLogin, db: Session):

        user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(
            user_data.password,
            user.password,
        ):
            raise ValueError("Invalid email or password")

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
            },
        }