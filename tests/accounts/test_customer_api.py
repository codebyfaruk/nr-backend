import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestCustomerAPI:

    def test_create_customer(self, staff_user):
        payload = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "Test Address"
        }
        url = reverse("api_customer-list")
        response = staff_user.post(url, payload)
        assert response.status_code == 201
        assert response.data["name"] == "Test Customer"

    def test_list_customers(self, staff_user, customer):
        url = reverse("api_customer-list")
        response = staff_user.get(url)
        assert response.status_code == 200
        assert any(c["name"] == customer.name for c in response.data)

    def test_retrieve_customer(self, staff_user, customer):
        url = reverse("api_customer-detail", kwargs={"pk": customer.id})
        response = staff_user.get(url)
        assert response.status_code == 200
        assert response.data["name"] == customer.name

    def test_update_customer(self, staff_user, customer):
        url = reverse("api_customer-detail", kwargs={"pk": customer.id})
        payload = {"name": "Updated Name"}
        response = staff_user.patch(url, payload)
        assert response.status_code == 200
        assert response.data["name"] == "Updated Name"

    def test_delete_customer(self, super_user, customer):
        url = reverse("api_customer-detail", kwargs={"pk": customer.id})
        response = super_user.delete(url)
        assert response.status_code == 204
