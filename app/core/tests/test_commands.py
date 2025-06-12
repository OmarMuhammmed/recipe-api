"""
Test custom Django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self):
        """Test waiting for database if database ready"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    def test_wait_for_db_delay(self):
        """Test waiting for database when getting OperationalError"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [Psycopg2Error] * 2 + \
                [OperationalError] * 3 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)