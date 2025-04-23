from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Provides `list`, `retrieve`, `create`, `update`, and `destroy`
    actions for the CustomUser model.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
