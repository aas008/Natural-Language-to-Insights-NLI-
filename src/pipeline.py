# src/pipeline.py

import os
import sys
import pandas as pd
from pathlib import Path

# Add the parent directory to sys.path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.sql_generator import SQLGenerator
from src.utils.schema_definitions import SchemaDefinition
from src.utils.query_executor import QueryExecutor
from src.visualization.visualizer import DataVisualizer
from src.insights.insights_generator import InsightsGenerator

class NLIpipeline:
    """End-to-end pipeline for Natural Language to Insights."""
    
    def __init__(self, api_key=None):
        """Initialize the pipeline components."""
        self.schema_def = SchemaDefinition()
        self.sql_generator = SQLGenerator(api_key)
        self.query_executor = QueryExecutor()
        self.visualizer = DataVisualizer()
        self.insights_generator = InsightsGenerator()
    
    def process(self, question, user_role="Analyst", domain="sales", csv_files=None):
        """
        Process a natural language question and generate insights.
        
        Args:
            question (str): Natural language question
            user_role (str): User role (e.g., "Sales Manager")
            domain (str): Data domain (e.g., "sales")
            csv_files (dict, optional): Mapping of table names to CSV files
            
        Returns:
            dict: Results including SQL, data, and visualization
        """
        # Step 1: Get schema information
        schema_text = self.schema_def.get_schema_text(domain)
        
        # Step 2: Generate SQL from natural language
        print(f"Generating SQL for: '{question}'")
        sql_query = self.sql_generator.generate_sql(question, schema_text, user_role)
        print(f"Generated SQL: {sql_query}")
        
        # Step 3: Execute the SQL query
        if csv_files is None:
            # If no files specified, infer from query or use default
            csv_files = {'sales': 'sales.csv'}
            if 'customers' in sql_query.lower():
                csv_files['customers'] = 'customers.csv'
                
        result_df = self.query_executor.execute_query(sql_query, csv_files)
        
        # Step 4: Generate visualization
        if not result_df.empty:
            viz_result = self.visualizer.visualize(result_df, question, user_role)
            print(f"Created visualization: {viz_result.get('type', 'unknown')} chart")
        else:
            viz_result = {"error": "No data to visualize"}
            print("No data available for visualization")
        
        if not result_df.empty:
            viz_result = self.visualizer.visualize(result_df, question, user_role)
            print(f"Created visualization: {viz_result.get('type', 'unknown')} chart")
            
            # Generate insights
            insights = self.insights_generator.generate_insights(
                result_df, 
                question, 
                viz_result.get('type', 'bar'),
                user_role
            )
            print(f"Generated insights: {insights.get('summary', '')[:100]}...")
        else:
            viz_result = {"error": "No data to visualize"}
            insights = {"summary": "No data available for analysis."}
            print("No data available for visualization or insights")

        # Prepare the complete results
        results = {
            "question": question,
            "user_role": user_role,
            "domain": domain,
            "sql_query": sql_query,
            "data": {
                "rows": len(result_df),
                "columns": list(result_df.columns),
                "preview": result_df.head(10).to_dict('records') if not result_df.empty else []
            },
            "visualization": viz_result,
            "insights": insights
        }


        
        return results

def test_full_pipeline():
    """Test the full NLI pipeline with some example questions."""
    # Create the pipeline
    pipeline = NLIpipeline()
    
    # Test questions
    test_questions = [
        {"question": "What are the sales by region?", "role": "Executive"},
        {"question": "Show me the top 5 products by revenue", "role": "Sales Manager"},
        {"question": "Which regions have the most customers?", "role": "Analyst"}
    ]
    
    print("=== Testing Full NLI Pipeline ===\n")
    
    for i, test in enumerate(test_questions):
        print(f"Test {i+1}: '{test['question']}' (Role: {test['role']})")
        
        # Process the question
        results = pipeline.process(test['question'], test['role'])
        
        # Display results
        print(f"SQL: {results['sql_query']}")
        print(f"Data: {results['data']['rows']} rows, {len(results['data']['columns'])} columns")
        
        if 'error' not in results['visualization']:
            print(f"Visualization: {results['visualization']['type']} chart saved to {results['visualization']['path']}")
        else:
            print(f"Visualization error: {results['visualization']['error']}")
        
        # Show a preview of the data
        if results['data']['preview']:
            print("\nData Preview:")
            preview_df = pd.DataFrame(results['data']['preview'])
            print(preview_df.head(5).to_string())
        
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    test_full_pipeline()