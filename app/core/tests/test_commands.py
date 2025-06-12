"""
Test custom Django management commands.
"""
from unittest.mock import patch, MagicMock

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    """Test commands."""

    @patch('core.management.commands.wait_for_db.connections')
    def test_wait_for_db_ready(self, patched_connections):
        """Test waiting for database if database ready."""
        # Mock the database connection to succeed immediately
        mock_cursor = MagicMock()
        patched_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        call_command('wait_for_db')

        # Verify the cursor.execute was called once
        mock_cursor.execute.assert_called_once_with('SELECT 1')

    @patch('time.sleep')
    @patch('core.management.commands.wait_for_db.connections')
    def test_wait_for_db_delay(self, patched_connections, patched_sleep):
        """Test waiting for database when getting OperationalError."""
        # Mock the database connection to fail several times then succeed
        mock_cursor = MagicMock()
        patched_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Configure side_effect: 2 Psycopg2 errors, 3 Django errors, then success
        mock_cursor.execute.side_effect = [
            Psycopg2OpError(),  # 1st call
            Psycopg2OpError(),  # 2nd call
            OperationalError(),  # 3rd call
            OperationalError(),  # 4th call
            OperationalError(),  # 5th call
            None  # 6th call succeeds
        ]

        call_command('wait_for_db')

        # Verify execute was called 6 times
        self.assertEqual(mock_cursor.execute.call_count, 6)
        # Verify sleep was called 5 times (once for each failure)
        self.assertEqual(patched_sleep.call_count, 5)