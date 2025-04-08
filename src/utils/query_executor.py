# src/utils/query_executor.py

import pandas as pd
import sqlite3
from contextlib import closing
import os

class QueryExecutor:
    """Execute SQL queries against CSV files using an in-memory SQLite database."""
    
    def __init__(self, data_dir=None):
        """
        Initialize the QueryExecutor.
        
        Args:
            data_dir (str, optional): Directory containing CSV files
        """
        if data_dir is None:
            # Default to a 'data' directory in the project root
            data_dir = os.getenv("DATA_DIR", "./data")
        self.data_dir = data_dir
    
    def load_csv(self, file_path, table_name=None):
        """
        Load a CSV file into a pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file
            table_name (str, optional): Name to use for the table in SQL queries
            
        Returns:
            pandas.DataFrame: Loaded data
        """
        # If file_path doesn't include the data_dir, prepend it
        if not os.path.isabs(file_path) and not file_path.startswith(self.data_dir):
            file_path = os.path.join(self.data_dir, file_path)
        
        # Load the CSV
        try:
            df = pd.read_csv(file_path)
            print(f"Loaded {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            print(f"Error loading CSV file {file_path}: {e}")
            return pd.DataFrame()
    
    def execute_query(self, sql_query, csv_files=None):
        """
        Execute an SQL query against one or more CSV files.
        
        Args:
            sql_query (str): SQL query to execute
            csv_files (dict, optional): Dictionary mapping table names to CSV file paths.
                                       If None, will try to infer from the query.
            
        Returns:
            pandas.DataFrame: Query results
        """
        if csv_files is None:
            csv_files = self._infer_tables_from_query(sql_query)
        
        # Create an in-memory SQLite database
        with closing(sqlite3.connect(':memory:')) as conn:
            # Load each CSV file into a table
            for table_name, file_path in csv_files.items():
                df = self.load_csv(file_path)
                df.to_sql(table_name, conn, index=False, if_exists='replace')
            
            # Execute the query
            try:
                result = pd.read_sql_query(sql_query, conn)
                print(f"Query returned {len(result)} rows")
                return result
            except Exception as e:
                print(f"Error executing query: {e}")
                return pd.DataFrame()
    
    def _infer_tables_from_query(self, sql_query):
        """
        Attempt to infer which tables are needed based on the SQL query.
        This is a simple implementation and might need to be enhanced.
        
        Args:
            sql_query (str): SQL query to analyze
            
        Returns:
            dict: Mapping of table names to file paths
        """
        # Simple implementation - looks for table names in the query
        # This won't handle all cases correctly but works for basic queries
        tables = {}
        
        # Common keywords followed by table names
        keywords = ['FROM', 'JOIN', 'INTO', 'UPDATE']
        
        # Convert to uppercase for case-insensitive matching
        query_upper = sql_query.upper()
        
        for keyword in keywords:
            # Find all occurrences of the keyword
            start_idx = 0
            while True:
                idx = query_upper.find(f" {keyword} ", start_idx)
                if idx == -1:
                    break
                
                # Extract the table name - this is a simplified approach
                start_pos = idx + len(keyword) + 2  # +2 for the spaces
                end_pos = query_upper.find(" ", start_pos)
                if end_pos == -1:
                    end_pos = len(query_upper)
                
                # Remove any non-alphanumeric characters
                table_name = query_upper[start_pos:end_pos].strip()
                table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
                
                if table_name and table_name not in tables:
                    # Assume there's a CSV file with the same name
                    tables[table_name.lower()] = f"{table_name.lower()}.csv"
                
                start_idx = end_pos
        
        # Default to 'sales.csv' if no tables found
        if not tables:
            tables['sales'] = 'sales.csv'
        
        return tables