from rest_framework.viewsets import ModelViewSet

from accounts.models import Customer, CustomUser
from accounts.serializers import CustomerSerializer, UserSerializer
from store.permissions import IsStaffPermission


class UserViewSet(ModelViewSet):
    """
    Provides `list`, `retrieve`, `create`, `update`, and `destroy`
    actions for the CustomUser model.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffPermission]


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsStaffPermission]
    allow_staff = True
