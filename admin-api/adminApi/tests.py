from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from .admin import match_choice, parse_coordinate
from .models import Pyme


class ImportHelpersTests(SimpleTestCase):
    def test_choice_matching_ignores_accents_and_case(self):
        self.assertEqual(
            match_choice("INNOVACION", Pyme.WorkTypeOptions.choices, "Trabajo"),
            Pyme.WorkTypeOptions.INNOVACION,
        )

    def test_coordinate_normalizes_decimal_comma(self):
        self.assertEqual(parse_coordinate("-34,60", -90, 90, "Latitud"), "-34.6")


class PymeModelTests(SimpleTestCase):
    def test_maturity_values_are_derived_from_score(self):
        pyme = Pyme(name="Ejemplo", maturity_score=Decimal("90"))
        self.assertEqual(pyme.maturity_level, 5)
        self.assertEqual(pyme.maturity_band, "Alto")
        self.assertEqual(pyme.rating, 4.5)


class ApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="owner@example.com", email="owner@example.com", password="A-secure-password-123"
        )
        self.pyme = Pyme.objects.create(
            name="Nodo Servicios",
            locality="Morón",
            province="Buenos Aires",
            work_type=Pyme.WorkTypeOptions.TRANSFORMACION_DIGITAL,
            enterprise_type=Pyme.EnterpriseTypeOptions.MICRO_PYME,
            sector=Pyme.SectorOptions.SERVICIOS,
            maturity_score=Decimal("96"),
            latitud="-34.65",
            longitud="-58.62",
        )
        self.client = APIClient()

    def test_api_requires_authentication(self):
        self.assertEqual(self.client.get("/api/pymes/").status_code, 401)

    def test_registration_and_email_login(self):
        registered = self.client.post(
            "/api/auth/register/",
            {"email": "new@example.com", "password": "Another-secure-password-123"},
            format="json",
        )
        self.assertEqual(registered.status_code, 201)
        login = self.client.post(
            "/api/token/",
            {"email": "new@example.com", "password": "Another-secure-password-123"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("access", login.data)

    def test_filters_summary_and_internal_models_are_not_exposed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/pymes/", {"search": "Nodo"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Nodo Servicios")
        summary = self.client.get("/api/pymes/summary/")
        self.assertEqual(summary.status_code, 200)
        self.assertEqual(summary.data["total_companies"], 1)
        self.assertEqual(summary.data["high_maturity_count"], 1)
        self.assertEqual(self.client.get("/api/users/").status_code, 404)
