# src/test_pipeline.py

from models.sql_generator import SQLGenerator
from utils.schema_definitions import SchemaDefinition

def test_pipeline():
    """Test the English-to-SQL pipeline with some sample questions."""
    schema_def = SchemaDefinition()
    sql_generator = SQLGenerator()
    
    schema_text = schema_def.get_schema_text("sales")
    
    test_questions = [
        ("What were total sales in 2024?", "Sales Manager"),
        ("Show me the top 5 products by revenue", "Executive"),
        ("What's the average sales amount per region?", "Analyst"),
        ("Compare sales between North and South regions", "Sales Manager")
    ]
    
    print("=== Testing English-to-SQL Pipeline ===\n")
    
    for question, role in test_questions:
        print(f"Question: {question}")
        print(f"User Role: {role}")
        
        sql = sql_generator.generate_sql(question, schema_text, role)
        
        print("\nGenerated SQL:")
        print(sql)
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    test_pipeline()