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
        call_command('wait_for_db')
        
        # Verify connections was accessed
        patched_connections.__getitem__.assert_called_with('default')

    @patch('time.sleep')
    @patch('core.management.commands.wait_for_db.connections')
    def test_wait_for_db_delay(self, patched_connections, patched_sleep):
        """Test waiting for database when getting OperationalError."""
        # Mock connection to raise exceptions on first 5 attempts, succeed on 6th
        mock_connection = MagicMock()
        patched_connections.__getitem__.return_value = mock_connection
        
        # Create side effect for cursor context manager
        def cursor_side_effect():
            mock_cursor_manager = MagicMock()
            return mock_cursor_manager
        
        # Set up the side effects - first 5 calls raise exceptions
        side_effects = [
            Psycopg2OpError(),  # 1st attempt
            Psycopg2OpError(),  # 2nd attempt  
            OperationalError(), # 3rd attempt
            OperationalError(), # 4th attempt
            OperationalError(), # 5th attempt
        ]
        
        attempt_count = 0
        def mock_cursor_context():
            nonlocal attempt_count
            attempt_count += 1
            
            if attempt_count <= 5:
                raise side_effects[attempt_count - 1]
            
            # 6th attempt succeeds
            mock_cursor_manager = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor_manager.__enter__.return_value = mock_cursor
            mock_cursor_manager.__exit__.return_value = None
            return mock_cursor_manager
        
        mock_connection.cursor.side_effect = mock_cursor_context

        call_command('wait_for_db')

        # Verify cursor was called 6 times
        self.assertEqual(mock_connection.cursor.call_count, 6)
        # Verify sleep was called 5 times (for each failure)
        self.assertEqual(patched_sleep.call_count, 5)