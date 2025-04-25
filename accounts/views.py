from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Customer, CustomUser
from accounts.serializers import CustomerSerializer, UserSerializer
from store.permissions import IsStaffPermission


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Incorrect username or password.",
        "inactive": "This account is inactive.",
    }


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


# Dashboard Views
class CustomerView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer_count"] = Customer.objects.count()
        return context


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    # If you want to add additional context (for example, error messages), you can override form_valid() or form_invalid().
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
