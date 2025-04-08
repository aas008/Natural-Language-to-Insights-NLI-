# src/utils/schema_definitions.py

class SchemaDefinition:
    """Class to manage and provide access to database schema definitions."""
    
    def __init__(self):
        # Default schemas - you can expand these or load from a file later
        self.schemas = {
            "sales": {
                "description": "Sales transaction data",
                "tables": {
                    "sales": {
                        "columns": {
                            "sale_id": {"type": "INTEGER", "description": "Unique identifier for each sale"},
                            "date": {"type": "DATE", "description": "Date of the sale"},
                            "product_name": {"type": "TEXT", "description": "Name of the product sold"},
                            "product_category": {"type": "TEXT", "description": "Category of the product"},
                            "quantity": {"type": "INTEGER", "description": "Number of units sold"},
                            "unit_price": {"type": "DECIMAL", "description": "Price per unit"},
                            "sales_amount": {"type": "DECIMAL", "description": "Total sale amount (quantity * unit_price)"},
                            "customer_id": {"type": "INTEGER", "description": "ID of the customer"},
                            "region": {"type": "TEXT", "description": "Geographic region of the sale"},
                            "sales_channel": {"type": "TEXT", "description": "Channel through which the sale was made"}
                        },
                        "primary_key": "sale_id"
                    },
                    "customers": {
                        "columns": {
                            "customer_id": {"type": "INTEGER", "description": "Unique identifier for each customer"},
                            "customer_name": {"type": "TEXT", "description": "Name of the customer"},
                            "segment": {"type": "TEXT", "description": "Customer segment (e.g., Consumer, Corporate)"},
                            "region": {"type": "TEXT", "description": "Customer's region"}
                        },
                        "primary_key": "customer_id"
                    }
                },
                "relationships": [
                    {
                        "from_table": "sales",
                        "from_column": "customer_id",
                        "to_table": "customers",
                        "to_column": "customer_id"
                    }
                ]
            }
        }
    
    def get_schema(self, domain="sales"):
        """Get the schema for a specific domain."""
        return self.schemas.get(domain, {})
    
    def get_schema_text(self, domain="sales"):
        """Convert schema to formatted text for LLM prompts."""
        schema = self.get_schema(domain)
        if not schema:
            return "No schema found for the specified domain."
        
        text = f"Domain: {domain}\n"
        text += f"Description: {schema.get('description', 'No description available')}\n\n"
        
        # Add tables
        for table_name, table_info in schema.get('tables', {}).items():
            text += f"Table: {table_name}\n"
            text += "Columns:\n"
            
            for col_name, col_info in table_info.get('columns', {}).items():
                text += f"  - {col_name} ({col_info.get('type', 'UNKNOWN')}): {col_info.get('description', '')}\n"
            
            if table_info.get('primary_key'):
                text += f"Primary Key: {table_info.get('primary_key')}\n"
            
            text += "\n"
        
        # Add relationships
        if schema.get('relationships'):
            text += "Relationships:\n"
            for rel in schema.get('relationships'):
                text += f"  - {rel.get('from_table')}.{rel.get('from_column')} -> {rel.get('to_table')}.{rel.get('to_column')}\n"
        
        return text