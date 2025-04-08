# src/test_visualization.py

import os
from pathlib import Path
import pandas as pd

# Add this to handle imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.query_executor import QueryExecutor
from src.visualization.visualizer import DataVisualizer
from src.insights.insights_generator import InsightsGenerator

def test_visualization():
    """Test the DataVisualizer with sample query results"""
    # Initialize components
    query_executor = QueryExecutor()
    visualizer = DataVisualizer()
    insights_generator = InsightsGenerator()
    
    # Test with some sample queries and visualizations
    test_cases = [
        {
            "description": "Bar chart for regional sales",
            "query": "SELECT region, SUM(sales_amount) as total_sales FROM sales GROUP BY region ORDER BY total_sales DESC",
            "files": {"sales": "sales.csv"},
            "viz_type": "bar",
            "title": "Total Sales by Region"
        },
        {
            "description": "Pie chart for product category breakdown",
            "query": "SELECT product_category, SUM(sales_amount) as total_sales FROM sales GROUP BY product_category",
            "files": {"sales": "sales.csv"},
            "viz_type": "pie",
            "title": "Sales by Product Category"
        },
        {
            "description": "Line chart for monthly trends (simulated)",
            "query": "WITH months AS (SELECT 1 as month UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6) " +
                    "SELECT months.month, SUM(CASE WHEN months.month = 1 THEN 100 WHEN months.month = 2 THEN 120 " +
                    "WHEN months.month = 3 THEN 160 WHEN months.month = 4 THEN 140 " +
                    "WHEN months.month = 5 THEN 190 WHEN months.month = 6 THEN 210 END) as sales " +
                    "FROM months GROUP BY months.month ORDER BY months.month",
            "files": {"sales": "sales.csv"},  # Not actually used, just required
            "viz_type": "line",
            "title": "Monthly Sales Trend"
        }
    ]
    
    print("=== Testing Visualization Module ===\n")
    
    for i, test_case in enumerate(test_cases):
        print(f"Test {i+1}: {test_case['description']}")
        print(f"SQL Query: {test_case['query']}")
        
        # Execute the query
        result_df = query_executor.execute_query(test_case['query'], test_case['files'])
        
        if not result_df.empty:
            print(f"Query returned {len(result_df)} rows")
            
            # Create visualization
            viz_result = visualizer.visualize(
                result_df, 
                test_case.get('query_text', test_case['query']),
                viz_type=test_case['viz_type'],
                title=test_case['title']
            )
            
            print(f"Visualization created: {viz_result.get('type')} chart")
            print(f"Saved to: {viz_result.get('path')}")
        else:
            print("No results to visualize")
        
        print("\n" + "-" * 50 + "\n")

        insights = insights_generator.generate_insights(
        result_df,
        test_case.get('query_text', test_case['query']),
        test_case['viz_type'],
        "Sales Manager"  # Example role
        )

        print("\nInsights:")
        print(insights['summary'])
        print("\nKey points:")
        for point in insights.get('key_points', []):
            print(f"- {point}")

        if 'role_specific' in insights:
            print("\nRole-specific insight:")
            print(insights['role_specific'])

if __name__ == "__main__":
    test_visualization()