import pytest
from accounts.serializers import UserSerializer
from accounts.models import CustomUser

@pytest.mark.django_db
class TestUserSerializer:

    def test_create_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
            "is_admin": True,
            "is_staff": False,
            "is_editor": True,
        }

        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        user = serializer.save()

        assert isinstance(user, CustomUser)
        assert user.username == data["username"]
        assert user.email == data["email"]
        assert user.is_admin is True
        assert user.is_staff is False
        assert user.is_editor is True
        # Password should be hashed
        assert user.check_password(data["password"]) is True
