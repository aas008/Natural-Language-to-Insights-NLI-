# src/visualization/visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import os

class DataVisualizer:
    """Generate appropriate visualizations based on query results."""
    
    def __init__(self, output_dir=None):
        """
        Initialize the visualizer.
        
        Args:
            output_dir (str, optional): Directory to save visualizations
        """
        if output_dir is None:
            output_dir = os.getenv("VISUALIZATION_DIR", "./output/visualizations")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set the style for visualizations
        sns.set_theme(style="whitegrid")
        
    def visualize(self, df, query_text, user_role=None, viz_type=None, title=None):
        """
        Create an appropriate visualization based on the data.
        
        Args:
            df (pandas.DataFrame): Data to visualize
            query_text (str): Original query text
            user_role (str, optional): User role for context-aware visualizations
            viz_type (str, optional): Force a specific visualization type
            title (str, optional): Custom title for the visualization
            
        Returns:
            dict: Visualization metadata including file path
        """
        if df.empty:
            return {"error": "No data to visualize"}
        
        # Determine the appropriate visualization type if not specified
        if viz_type is None:
            viz_type = self._recommend_visualization(df, query_text)
        
        # Create a unique filename
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{viz_type}_{timestamp}.png"
        file_path = self.output_dir / file_name
        
        # Generate the title if not provided
        if title is None:
            title = self._generate_title(query_text, df.columns)
        
        # Create the visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            if viz_type == "bar":
                self._create_bar_chart(df, ax)
            elif viz_type == "line":
                self._create_line_chart(df, ax)
            elif viz_type == "pie":
                self._create_pie_chart(df, ax)
            elif viz_type == "scatter":
                self._create_scatter_plot(df, ax)
            elif viz_type == "heatmap":
                self._create_heatmap(df, ax)
            else:
                # Default to a table for small datasets or unknown types
                self._create_table_visualization(df, ax)
            
            # Add title and labels
            plt.title(title, fontsize=14, pad=20)
            plt.tight_layout()
            
            # Save the figure
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            return {
                "type": viz_type,
                "path": str(file_path),
                "title": title,
                "data_shape": df.shape
            }
            
        except Exception as e:
            plt.close(fig)
            print(f"Error creating visualization: {e}")
            return {"error": str(e)}
    
    def _recommend_visualization(self, df, query_text):
        """
        Recommend an appropriate visualization type based on the data and query.
        
        Args:
            df (pandas.DataFrame): Data to visualize
            query_text (str): Original query text
            
        Returns:
            str: Recommended visualization type
        """
        # Check for keywords in the query text
        query_lower = query_text.lower()
        
        # Check for time series related keywords
        time_keywords = ["trend", "over time", "by month", "by year", "by quarter", "monthly", "yearly", "quarterly"]
        if any(keyword in query_lower for keyword in time_keywords):
            return "line"
        
        # Check for comparison keywords
        comparison_keywords = ["compare", "comparison", "versus", "vs", "difference between"]
        if any(keyword in query_lower for keyword in comparison_keywords):
            return "bar"
        
        # Check for distribution keywords
        distribution_keywords = ["distribution", "spread", "range"]
        if any(keyword in query_lower for keyword in distribution_keywords):
            return "histogram"
        
        # Check for correlation keywords
        correlation_keywords = ["correlation", "relationship", "scatter", "between"]
        if any(keyword in query_lower for keyword in correlation_keywords) and df.shape[1] >= 3:
            return "scatter"
        
        # Check for proportion keywords
        proportion_keywords = ["proportion", "percentage", "share", "ratio", "breakdown", "composition"]
        if any(keyword in query_lower for keyword in proportion_keywords):
            return "pie"
        
        # Make recommendations based on data structure
        num_rows, num_cols = df.shape
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # For 2 columns with one categorical and one numeric
        if num_cols == 2 and len(numeric_cols) == 1:
            categorical_col = [col for col in df.columns if col not in numeric_cols][0]
            # If few categories, use pie chart
            if df[categorical_col].nunique() <= 6 and df[categorical_col].nunique() > 1:
                return "pie"
            # Otherwise use bar chart
            else:
                return "bar"
        
        # For data with datetime and numeric columns, prefer line charts
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'year' in col.lower()]
        if date_cols and len(numeric_cols) >= 1:
            return "line"
        
        # For categorical data with numeric values, use bar charts
        if len(numeric_cols) >= 1 and num_cols >= 2:
            return "bar"
        
        # For matrices/cross-tabs, use heatmaps
        if num_cols >= 3 and num_rows >= 3 and df.dtypes.nunique() <= 2:
            return "heatmap"
        
        # Default to bar chart for most cases
        return "bar"
    
    def _generate_title(self, query_text, columns):
        """Generate a title based on the query and columns."""
        # Simple title generation - capitalize first letter and add a period if missing
        title = query_text.strip()
        title = title[0].upper() + title[1:]
        if not title.endswith((".", "!", "?")):
            title += "."
        return title
    
    def _create_bar_chart(self, df, ax):
        """Create a bar chart."""
        # Identify the categorical and numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        
        if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
            # Use the first non-numeric column for x-axis
            x_col = non_numeric_cols[0]
            # Use the first numeric column for y-axis
            y_col = numeric_cols[0]
            
            # Sort by the y-axis value in descending order
            df_sorted = df.sort_values(by=y_col, ascending=False)
            
            # Limit to top 15 for readability
            if len(df_sorted) > 15:
                df_sorted = df_sorted.head(15)
                ax.set_title("Top 15 results", fontsize=10)
            
            # Create the bar chart
            sns.barplot(data=df_sorted, x=x_col, y=y_col, ax=ax)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
        else:
            # Default case - use the index as x-axis
            df.plot(kind='bar', ax=ax)
    
    def _create_line_chart(self, df, ax):
        """Create a line chart."""
        # Look for date columns
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'year' in col.lower()]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if date_cols and len(numeric_cols) >= 1:
            # Use the first date column for x-axis
            x_col = date_cols[0]
            # Use the first numeric column for y-axis
            y_col = numeric_cols[0]
            
            # Sort by the date column
            df_sorted = df.sort_values(by=x_col)
            
            # Plot the line chart
            plt.plot(df_sorted[x_col], df_sorted[y_col], marker='o', linestyle='-')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.xticks(rotation=45)
        else:
            # Default line chart using all columns
            df.plot(kind='line', ax=ax)
    
    def _create_pie_chart(self, df, ax):
        """Create a pie chart."""
        # Identify the categorical and numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        
        if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1:
            # Use the first non-numeric column for labels
            label_col = non_numeric_cols[0]
            # Use the first numeric column for values
            value_col = numeric_cols[0]
            
            # Limit to top 8 categories for readability
            if len(df) > 8:
                df = df.nlargest(8, value_col)
                plt.title("Top 8 categories", fontsize=10)
            
            # Create the pie chart
            ax.pie(df[value_col], labels=df[label_col], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        else:
            # Default pie chart using the first column
            df.iloc[:, 0].plot(kind='pie', ax=ax)
    
    def _create_scatter_plot(self, df, ax):
        """Create a scatter plot."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            # Use the first two numeric columns
            x_col = numeric_cols[0]
            y_col = numeric_cols[1]
            
            # Create the scatter plot
            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
            
            # Add a trend line
            sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ax=ax, color='red')
            
            plt.xlabel(x_col)
            plt.ylabel(y_col)
        else:
            # Default scatter plot using all columns
            df.plot(kind='scatter', x=df.columns[0], y=df.columns[-1], ax=ax)
    
    def _create_heatmap(self, df, ax):
        """Create a heatmap."""
        # Convert all columns to numeric if possible
        df_numeric = df.apply(pd.to_numeric, errors='coerce')
        
        # Create the heatmap
        sns.heatmap(df_numeric, annot=True, cmap='viridis', fmt='.2f', ax=ax)
    
    def _create_table_visualization(self, df, ax):
        """Create a table visualization."""
        # Hide axes
        ax.axis('off')
        
        # Limit to 20 rows for readability
        if len(df) > 20:
            df = df.head(20)
        
        # Create the table
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center',
            bbox=[0, 0, 1, 1]
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)