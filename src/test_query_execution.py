# src/test_query_execution.py

import os
from pathlib import Path

# Add this to handle imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.query_executor import QueryExecutor
from src.models.sql_generator import SQLGenerator
from src.utils.schema_definitions import SchemaDefinition

def create_sample_data():
    """Create a sample CSV file for testing"""
    import pandas as pd
    import numpy as np
    
    # Create data directory if it doesn't exist
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)
    
    # Create sample sales data
    sales_data = {
        'sale_id': range(1, 101),
        'date': pd.date_range(start='2024-01-01', periods=100),
        'product_name': np.random.choice(['Laptop Pro', 'Smartphone X', 'Tablet Y', 'Desktop Z', 'Monitor'], 100),
        'product_category': np.random.choice(['Electronics', 'Accessories'], 100),
        'quantity': np.random.randint(1, 10, 100),
        'unit_price': np.random.uniform(100, 1500, 100).round(2),
        'customer_id': np.random.randint(1, 21, 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'sales_channel': np.random.choice(['Online', 'Retail', 'Distributor'], 100)
    }
    
    # Calculate sales_amount
    sales_df = pd.DataFrame(sales_data)
    sales_df['sales_amount'] = (sales_df['quantity'] * sales_df['unit_price']).round(2)
    
    # Save to CSV
    sales_df.to_csv(data_dir / "sales.csv", index=False)
    print(f"Created sample sales data with {len(sales_df)} rows")
    
    # Create sample customer data
    customer_data = {
        'customer_id': range(1, 21),
        'customer_name': [f"Customer {i}" for i in range(1, 21)],
        'segment': np.random.choice(['Consumer', 'Corporate', 'Small Business'], 20),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 20)
    }
    
    customer_df = pd.DataFrame(customer_data)
    customer_df.to_csv(data_dir / "customers.csv", index=False)
    print(f"Created sample customer data with {len(customer_df)} rows")

def test_query_execution():
    """Test the QueryExecutor with some sample queries"""
    # Create sample data if it doesn't exist
    if not os.path.exists("data/sales.csv"):
        create_sample_data()
    
    # Initialize components
    query_executor = QueryExecutor()
    schema_def = SchemaDefinition()
    
    # Test with some predefined SQL queries
    test_queries = [
        "SELECT region, SUM(sales_amount) as total_sales FROM sales GROUP BY region ORDER BY total_sales DESC",
        "SELECT product_name, SUM(quantity) as units_sold FROM sales GROUP BY product_name ORDER BY units_sold DESC LIMIT 5",
        "SELECT s.region, COUNT(DISTINCT s.customer_id) as customer_count FROM sales s GROUP BY s.region"
    ]
    
    print("=== Testing Query Execution ===\n")
    
    for sql in test_queries:
        print(f"SQL Query: {sql}")
        
        # Execute the query
        result = query_executor.execute_query(sql, {'sales': 'sales.csv'})
        
        # Display the result
        if not result.empty:
            print("\nResult:")
            print(result.head().to_string())
            print(f"Total rows: {len(result)}")
        else:
            print("No results returned")
        
        print("\n" + "-" * 50 + "\n")
    
    # Test with a generated SQL query
    try:
        sql_generator = SQLGenerator()  # You'll need your API key set up for this
        schema_text = schema_def.get_schema_text("sales")
        
        nl_query = "What are the total sales for each product category in the North region?"
        print(f"Natural Language Query: {nl_query}")
        
        # Generate SQL
        sql = sql_generator.generate_sql(nl_query, schema_text, "Sales Manager")
        print(f"Generated SQL: {sql}")
        
        # Execute the query
        result = query_executor.execute_query(sql, {'sales': 'sales.csv'})
        
        # Display the result
        if not result.empty:
            print("\nResult:")
            print(result.to_string())
        else:
            print("No results returned")
            
    except Exception as e:
        print(f"Error in SQL generation: {e}")

if __name__ == "__main__":
    test_query_execution()