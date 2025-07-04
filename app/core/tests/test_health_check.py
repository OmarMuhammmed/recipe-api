from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    """Test the health check API"""

    def test_health_check(self):
        """Test that the health check works"""
        client = APIClient()
        url = reverse('health-check')
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
