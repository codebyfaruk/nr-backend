import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Customer  

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserView:
    def test_str_returns_username(self):
        user = User.objects.create_user(username="testuser", password="pass123")
        assert str(user) == "testuser"

    def test_create_admin_and_editor_flags(self):
        user = User.objects.create_user(username="admin", password="pass123", is_admin=True, is_editor=True)
        assert user.is_admin is True
        assert user.is_editor is True


@pytest.mark.django_db
class TestLoginLogout:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpass")

    def test_login_success(self, client, user):
        url = reverse("login")
        response = client.post(url, {"username": "testuser", "password": "testpass"})
        assert response.status_code == 302  # Redirect on success
        assert response.url == reverse("home")

    def test_login_failure(self, client):
        url = reverse("login")
        response = client.post(url, {"username": "wrong", "password": "wrong"})
        assert response.status_code == 200
        assert "form" in response.context
        form = response.context["form"]

        assert form.errors
        assert "__all__" in form.errors
        assert "Incorrect username or password" in form.errors["__all__"][0]

    def test_logout_redirects_to_login(self, client, user):
        client.force_login(user)
        url = reverse("logout")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse("login")



@pytest.mark.django_db
class TestCustomerView:
    def test_str_returns_name(self):
        customer = Customer.objects.create(name="John Smith")
        assert str(customer) == "John Smith"

    
    @pytest.mark.django_db
    def test_customer_view_context(self, staff_user):
        # Create a user for authentication (if needed)
        # Create 3 customers for testing
        for i in range(3):
            Customer.objects.create(name=f"Customer {i}", email=f"c{i}@example.com")
        url = reverse("customer_view")
        response = staff_user.get(url)
        assert response.status_code == 200
        assert response.context['customer_count'] == 3