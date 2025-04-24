from rest_framework import serializers

from accounts.models import Customer, CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "is_admin",
            "is_staff",
            "is_editor",
            "password",
        ]

    def create(self, validated_data):
        # Create a new user instance
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            is_admin=validated_data.get("is_admin", False),
            is_staff=validated_data.get("is_staff", False),
            is_editor=validated_data.get("is_editor", False),
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
