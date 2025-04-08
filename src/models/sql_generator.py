# src/models/sql_generator.py

import os
import requests
from dotenv import load_dotenv

class SQLGenerator:
    """Generates SQL queries from natural language using LLMs."""
    
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("Hugging Face API key is required. Set HUGGINGFACE_API_KEY in .env or pass directly.")
        
        # Default to a good SQL generation model
        self.model_url = os.getenv("HF_MODEL_URL", "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2")
    
    def generate_sql(self, question, schema_text, user_role):
        """
        Generate SQL from natural language question.
        
        Args:
            question (str): Natural language question
            schema_text (str): Database schema in text format
            user_role (str): User role (e.g., "Sales Manager")
            
        Returns:
            str: Generated SQL query
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        You are an expert SQL query generator for a business intelligence system.
        
        DATABASE SCHEMA:
        {schema_text}
        
        USER ROLE: {user_role}
        
        USER QUESTION: {question}
        
        Generate a valid SQL query that answers the user's question based on the provided schema.
        Return ONLY the SQL query, without any explanations or markdown formatting.
        """
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.1,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.model_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract the generated SQL
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            else:
                generated_text = str(result)
            
            # Clean up the output
            sql_query = self._clean_sql(generated_text)
            return sql_query
            
        except Exception as e:
            print(f"Error generating SQL: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return f"Error: {str(e)}"
    
    def _clean_sql(self, text):
        """Clean the generated SQL output."""
        # Remove any markdown formatting
        if "```sql" in text:
            text = text.split("```sql")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
        
        # Ensure the output starts with SQL keywords
        lines = text.split("\n")
        sql_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("--"):  # Skip comment lines
                sql_lines.append(line)
        
        return "\n".join(sql_lines)