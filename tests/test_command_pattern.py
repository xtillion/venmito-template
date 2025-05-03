# tests/test_command_pattern.py
import unittest
import pandas as pd
from src.commands.process_data_command import ProcessDataCommand, MergeDataCommand
from src.commands.command_invoker import CommandInvoker

class TestCommandPattern(unittest.TestCase):
    def test_process_data_command(self):
        """Test processing people data using the command pattern."""
        # Create a sample DataFrame for people
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com']
        })
        
        # Create and execute the command
        command = ProcessDataCommand(df, 'people')
        invoker = CommandInvoker()
        result = invoker.execute_command(command)
        
        # Verify the result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('user_id', result.columns)  # 'id' should be renamed to 'user_id'
        
        # Verify the command was added to the history
        self.assertEqual(len(invoker.get_history()), 1)
        self.assertIs(invoker.get_history()[0], command)
    
    def test_merge_data_command(self):
        """Test merging people data using the command pattern."""
        # Create sample DataFrames for people from JSON and YAML
        json_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com']
        })
        
        yml_df = pd.DataFrame({
            'id': [4, 5],
            'name': ['Alice Williams', 'Dave Brown'],
            'email': ['alice@example.com', 'dave@example.com']
        })
        
        # Create and execute the command
        command = MergeDataCommand(json_df, yml_df)
        invoker = CommandInvoker()
        result = invoker.execute_command(command)
        
        # Verify the result
        self.assertIsInstance(result, dict)
        self.assertIn('people', result)
        self.assertIsInstance(result['people'], pd.DataFrame)
        
        # The merged DataFrame should have all 5 people
        self.assertEqual(len(result['people']), 5)
        
        # Verify the command was added to the history
        self.assertEqual(len(invoker.get_history()), 1)
        self.assertIs(invoker.get_history()[0], command)

if __name__ == '__main__':
    unittest.main()