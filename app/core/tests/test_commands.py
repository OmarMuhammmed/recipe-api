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

    @patch('django.db.connections["default"].cursor')
    def test_wait_for_db_ready(self, patched_cursor):
        """Test waiting for database if database ready"""
        patched_cursor.return_value.__enter__.return_value = True

        call_command('wait_for_db')

        patched_cursor.assert_called_once()

    @patch('time.sleep')
    @patch('django.db.connections["default"].cursor')
    def test_wait_for_db_delay(self, patched_cursor, patched_sleep):
        """Test waiting for database when getting OperationalError"""
        patched_cursor.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_cursor.call_count, 6)