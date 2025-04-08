# src/cli.py

import argparse
import os
from dotenv import load_dotenv
from models.sql_generator import SQLGenerator
from utils.schema_definitions import SchemaDefinition

def main():
    """Command-line interface for Natural Language to SQL conversion."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Convert natural language to SQL')
    parser.add_argument('--question', '-q', type=str, help='Natural language question')
    parser.add_argument('--role', '-r', type=str, default='Analyst', help='User role (default: Analyst)')
    parser.add_argument('--domain', '-d', type=str, default='sales', help='Data domain (default: sales)')
    
    args = parser.parse_args()
    
    # If no question provided, enter interactive mode
    if not args.question:
        print("=== Natural Language to SQL Converter ===")
        print("Enter 'exit' to quit")
        print()
        
        schema_def = SchemaDefinition()
        sql_generator = SQLGenerator()
        
        while True:
            role = input("User role (default: Analyst): ") or "Analyst"
            domain = input("Data domain (default: sales): ") or "sales"
            
            schema_text = schema_def.get_schema_text(domain)
            print("\nSchema loaded. You can now ask questions.")
            
            while True:
                question = input("\nQuestion (or 'change' to switch role/domain, 'exit' to quit): ")
                if question.lower() == 'exit':
                    return
                if question.lower() == 'change':
                    break
                
                print("\nGenerating SQL...")
                sql = sql_generator.generate_sql(question, schema_text, role)
                
                print("\n=== Generated SQL ===")
                print(sql)
                print("====================\n")
    
    else:
        # One-off conversion
        schema_def = SchemaDefinition()
        schema_text = schema_def.get_schema_text(args.domain)
        
        sql_generator = SQLGenerator()
        sql = sql_generator.generate_sql(args.question, schema_text, args.role)
        
        print(sql)

if __name__ == "__main__":
    main()