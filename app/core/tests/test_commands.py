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

    @patch('django.db.connections')
    def test_wait_for_db_ready(self, patched_connections):
        """Test waiting for database if database ready"""
        patched_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value = True

        call_command('wait_for_db')

        patched_connections.__getitem__.assert_called_once_with('default')

    @patch('time.sleep')
    @patch('django.db.connections')
    def test_wait_for_db_delay(self, patched_connections, patched_sleep):
        """Test waiting for database when getting OperationalError"""
        patched_connections.__getitem__.return_value.cursor.side_effect = [
            Psycopg2Error,
            Psycopg2Error,
            OperationalError,
            OperationalError,
            OperationalError,
            True
        ]

        call_command('wait_for_db')

        self.assertEqual(patched_connections.__getitem__.call_count, 6)
        patched_connections.__getitem__.assert_called_with('default')