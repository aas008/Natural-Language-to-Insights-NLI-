# src/insights/insights_generator.py

import pandas as pd
import numpy as np
from datetime import datetime

class InsightsGenerator:
    """Generate natural language insights from query results."""
    
    def generate_insights(self, df, query_text, viz_type, user_role=None):
        """
        Generate insights based on the data and visualization type.
        
        Args:
            df (pandas.DataFrame): The query result data
            query_text (str): The original natural language query
            viz_type (str): The type of visualization created
            user_role (str, optional): The user's role for contextual insights
            
        Returns:
            dict: Dictionary containing insights and metadata
        """
        if df.empty:
            return {"summary": "No data available for analysis."}
        
        # Basic data examination
        num_rows, num_cols = df.shape
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Generate insights based on visualization type
        if viz_type == "bar":
            insights = self._generate_bar_chart_insights(df, query_text)
        elif viz_type == "line":
            insights = self._generate_line_chart_insights(df, query_text)
        elif viz_type == "pie":
            insights = self._generate_pie_chart_insights(df, query_text)
        elif viz_type == "scatter":
            insights = self._generate_scatter_plot_insights(df, query_text)
        else:
            insights = self._generate_general_insights(df, query_text)
        
        # Add role-specific insights if user_role is provided
        if user_role:
            role_insights = self._add_role_specific_insights(df, insights["summary"], user_role)
            insights["role_specific"] = role_insights
        
        return insights
    
    def _generate_bar_chart_insights(self, df, query_text):
        """Generate insights for bar charts."""
        insights = {"summary": "", "key_points": []}
        
        try:
            # Identify likely value column (usually the 2nd column in the result)
            value_col = df.select_dtypes(include=[np.number]).columns[0] if len(df.select_dtypes(include=[np.number]).columns) > 0 else df.columns[1]
            category_col = [col for col in df.columns if col != value_col][0] if len(df.columns) > 1 else df.columns[0]
            
            # Basic statistics
            total = df[value_col].sum()
            average = df[value_col].mean()
            
            # Identify top and bottom performers
            top_category = df.iloc[df[value_col].argmax()]
            bottom_category = df.iloc[df[value_col].argmin()]
            
            # Calculate percentage of top category from total
            top_percentage = (top_category[value_col] / total) * 100 if total > 0 else 0
            
            # Generate summary
            summary = f"Analysis shows that {top_category[category_col]} leads with {top_category[value_col]:,.2f} "
            summary += f"({top_percentage:.1f}% of total), while {bottom_category[category_col]} "
            summary += f"has the lowest value at {bottom_category[value_col]:,.2f}. "
            
            # Add comparison to average if there are multiple categories
            if len(df) > 2:
                above_avg = df[df[value_col] > average][category_col].tolist()
                if len(above_avg) > 0:
                    if len(above_avg) == 1:
                        summary += f"Only {above_avg[0]} performs above the average of {average:,.2f}."
                    else:
                        summary += f"{len(above_avg)} out of {len(df)} categories perform above the average of {average:,.2f}."
            
            insights["summary"] = summary
            
            # Add key points
            insights["key_points"] = [
                f"Total {value_col}: {total:,.2f}",
                f"Average {value_col} per {category_col}: {average:,.2f}",
                f"Top performer: {top_category[category_col]} with {top_category[value_col]:,.2f}",
                f"Bottom performer: {bottom_category[category_col]} with {bottom_category[value_col]:,.2f}"
            ]
            
            # Add spread insight
            spread = df[value_col].max() - df[value_col].min()
            spread_percentage = (spread / df[value_col].min()) * 100 if df[value_col].min() > 0 else 0
            if spread_percentage > 100:
                insights["key_points"].append(f"Wide performance gap: {spread_percentage:.1f}% difference between top and bottom performers")
            
            # Add distribution insight if there are enough categories
            if len(df) >= 4:
                median = df[value_col].median()
                if median < average:
                    insights["key_points"].append("Distribution is skewed, with a few high performers pulling up the average")
            
        except Exception as e:
            insights["summary"] = f"The chart shows the distribution across different {category_col} values."
            insights["error"] = str(e)
        
        return insights
    
    def _generate_pie_chart_insights(self, df, query_text):
        """Generate insights for pie charts."""
        insights = {"summary": "", "key_points": []}
        
        try:
            # Identify likely value column (usually the 2nd column in the result)
            value_col = df.select_dtypes(include=[np.number]).columns[0] if len(df.select_dtypes(include=[np.number]).columns) > 0 else df.columns[1]
            category_col = [col for col in df.columns if col != value_col][0] if len(df.columns) > 1 else df.columns[0]
            
            # Calculate total and percentages
            total = df[value_col].sum()
            df['percentage'] = (df[value_col] / total) * 100
            
            # Get top categories
            top_categories = df.nlargest(2, value_col)
            top_combined_pct = top_categories['percentage'].sum()
            
            # Generate summary
            if len(df) <= 3:
                # For few categories, mention all
                category_insights = []
                for _, row in df.iterrows():
                    category_insights.append(f"{row[category_col]} ({row['percentage']:.1f}%)")
                summary = f"The breakdown shows: {', '.join(category_insights)}."
            else:
                # For many categories, focus on top ones
                summary = f"The top two categories, {top_categories.iloc[0][category_col]} and {top_categories.iloc[1][category_col]}, "
                summary += f"account for {top_combined_pct:.1f}% of the total."
                
                # Add insight about concentration
                if top_combined_pct > 75:
                    summary += f" This indicates a high concentration in these categories."
                elif top_combined_pct < 40:
                    summary += f" This suggests a relatively even distribution across categories."
            
            insights["summary"] = summary
            
            # Add key points
            insights["key_points"] = [
                f"Total {value_col}: {total:,.2f}",
                f"Largest segment: {top_categories.iloc[0][category_col]} ({top_categories.iloc[0]['percentage']:.1f}%)",
                f"Number of categories: {len(df)}"
            ]
            
            # Add distribution insight
            if len(df) > 3:
                small_categories = df[df['percentage'] < 5]
                if len(small_categories) > 0:
                    insights["key_points"].append(f"{len(small_categories)} categories account for less than 5% each")
            
        except Exception as e:
            insights["summary"] = f"The chart shows the proportional breakdown across different {category_col} values."
            insights["error"] = str(e)
        
        return insights
    
    def _generate_line_chart_insights(self, df, query_text):
        """Generate insights for line charts."""
        insights = {"summary": "", "key_points": []}
        
        try:
            # Identify likely time and value columns
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'month' in col.lower() or 'year' in col.lower()]
            time_col = date_cols[0] if date_cols else df.columns[0]
            value_col = df.select_dtypes(include=[np.number]).columns[0] if len(df.select_dtypes(include=[np.number]).columns) > 0 else df.columns[1]
            
            # Sort by time column
            df_sorted = df.sort_values(by=time_col)
            
            # Calculate basic metrics
            latest_value = df_sorted[value_col].iloc[-1]
            earliest_value = df_sorted[value_col].iloc[0]
            max_value = df_sorted[value_col].max()
            max_point = df_sorted.loc[df_sorted[value_col].idxmax()]
            
            # Calculate change
            absolute_change = latest_value - earliest_value
            percent_change = (absolute_change / earliest_value) * 100 if earliest_value != 0 else 0
            
            # Determine trend direction
            if percent_change > 5:
                trend = "upward"
            elif percent_change < -5:
                trend = "downward"
            else:
                trend = "stable"
            
            # Generate summary
            summary = f"The data shows a {trend} trend with a {abs(percent_change):.1f}% "
            summary += f"{'increase' if percent_change >= 0 else 'decrease'} "
            summary += f"from {earliest_value:,.2f} to {latest_value:,.2f}. "
            
            # Add peak information
            if max_value != latest_value and max_value != earliest_value:
                summary += f"The highest point was {max_value:,.2f} at {max_point[time_col]}."
            
            insights["summary"] = summary
            
            # Add key points
            insights["key_points"] = [
                f"Overall change: {absolute_change:+,.2f} ({percent_change:+.1f}%)",
                f"Starting value: {earliest_value:,.2f}",
                f"Ending value: {latest_value:,.2f}",
                f"Peak value: {max_value:,.2f} at {max_point[time_col]}"
            ]
            
            # Add volatility insight if enough data points
            if len(df) >= 4:
                std_dev = df_sorted[value_col].std()
                mean = df_sorted[value_col].mean()
                coef_variation = (std_dev / mean) * 100 if mean != 0 else 0
                
                if coef_variation > 20:
                    insights["key_points"].append(f"High volatility detected (CV: {coef_variation:.1f}%)")
                elif coef_variation < 5:
                    insights["key_points"].append(f"Very stable trend with minimal fluctuation (CV: {coef_variation:.1f}%)")
            
        except Exception as e:
            insights["summary"] = f"The chart tracks changes in {value_col} over time."
            insights["error"] = str(e)
        
        return insights
    
    def _generate_scatter_plot_insights(self, df, query_text):
        """Generate insights for scatter plots."""
        insights = {"summary": "", "key_points": []}
        
        try:
            # Identify the numeric columns for correlation
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                x_col = numeric_cols[0]
                y_col = numeric_cols[1]
                
                # Calculate correlation
                correlation = df[x_col].corr(df[y_col])
                
                # Generate summary based on correlation strength
                if abs(correlation) > 0.7:
                    strength = "strong"
                elif abs(correlation) > 0.3:
                    strength = "moderate"
                else:
                    strength = "weak"
                
                direction = "positive" if correlation > 0 else "negative"
                
                summary = f"There is a {strength} {direction} correlation ({correlation:.2f}) "
                summary += f"between {x_col} and {y_col}. "
                
                if correlation > 0.5:
                    summary += f"As {x_col} increases, {y_col} tends to increase as well."
                elif correlation < -0.5:
                    summary += f"As {x_col} increases, {y_col} tends to decrease."
                else:
                    summary += f"The relationship between these variables is not very pronounced."
                
                insights["summary"] = summary
                
                # Add key points
                insights["key_points"] = [
                    f"Correlation coefficient: {correlation:.2f}",
                    f"Sample size: {len(df)} data points"
                ]
                
                # Add outlier insight if applicable
                x_mean, x_std = df[x_col].mean(), df[x_col].std()
                y_mean, y_std = df[y_col].mean(), df[y_col].std()
                
                outliers = df[((df[x_col] > x_mean + 2*x_std) | 
                              (df[x_col] < x_mean - 2*x_std) | 
                              (df[y_col] > y_mean + 2*y_std) | 
                              (df[y_col] < y_mean - 2*y_std))]
                
                if len(outliers) > 0:
                    insights["key_points"].append(f"Contains {len(outliers)} potential outliers that may affect the correlation")
            else:
                insights["summary"] = "The scatter plot shows the relationship between two variables."
        
        except Exception as e:
            insights["summary"] = "The scatter plot shows the relationship between two variables."
            insights["error"] = str(e)
        
        return insights
    
    def _generate_general_insights(self, df, query_text):
        """Generate general insights for any data."""
        insights = {"summary": "", "key_points": []}
        
        try:
            # Basic data profiling
            num_rows, num_cols = df.shape
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            # Generate basic summary
            summary = f"The query returned {num_rows} results with {num_cols} columns. "
            
            # Add numeric column insights if available
            if numeric_cols:
                # Get the first numeric column for basic stats
                main_col = numeric_cols[0]
                total = df[main_col].sum()
                avg = df[main_col].mean()
                
                summary += f"The total {main_col} is {total:,.2f} with an average of {avg:,.2f}."
            else:
                # For non-numeric data, give column information
                summary += f"The data contains categorical information across {', '.join(df.columns.tolist())}."
            
            insights["summary"] = summary
            
            # Add key points about the data
            insights["key_points"] = [
                f"Number of records: {num_rows}",
                f"Number of columns: {num_cols}"
            ]
            
            # Add information about missing values if any
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                insights["key_points"].append(f"Contains {missing_values} missing values")
            
            # Add information about unique values in the first column
            first_col = df.columns[0]
            unique_count = df[first_col].nunique()
            insights["key_points"].append(f"{unique_count} unique values in '{first_col}' column")
            
        except Exception as e:
            insights["summary"] = "The data shows results from your query."
            insights["error"] = str(e)
        
        return insights
    
    def _add_role_specific_insights(self, df, base_summary, user_role):
        """Add role-specific insights based on user role."""
        role_insights = ""
        
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if user_role.lower() == "sales manager":
                # Sales manager cares about top performers and growth opportunities
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    if 'region' in df.columns:
                        top_region = df.nlargest(1, value_col)['region'].iloc[0]
                        role_insights = f"As a Sales Manager, focus on replicating the success in {top_region} "
                        role_insights += f"across other regions to maximize overall performance."
                    elif 'product' in df.columns or any('product' in col.lower() for col in df.columns):
                        prod_col = [col for col in df.columns if 'product' in col.lower()][0]
                        top_product = df.nlargest(1, value_col)[prod_col].iloc[0]
                        role_insights = f"As a Sales Manager, consider expanding the marketing efforts for {top_product} "
                        role_insights += f"given its strong performance."
                    else:
                        role_insights = "As a Sales Manager, analyze which factors contribute to the top performers and apply those strategies more broadly."
            
            elif user_role.lower() == "executive":
                # Executives care about high-level trends and business impact
                role_insights = "From an executive perspective, this data suggests "
                
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    total = df[value_col].sum()
                    
                    if total > 0:
                        # Check for concentration risk
                        top_concentration = df.nlargest(1, value_col)[value_col].iloc[0] / total * 100
                        if top_concentration > 40:
                            role_insights += f"a potential concentration risk with {top_concentration:.1f}% "
                            role_insights += f"of total {value_col} coming from a single source. Consider diversification strategies."
                        else:
                            role_insights += "a balanced distribution that aligns with the company's diversification goals."
                    else:
                        role_insights += "areas that need strategic attention to improve overall performance."
                else:
                    role_insights += "areas that warrant strategic review based on the categorical distribution shown."
            
            elif user_role.lower() == "finance":
                # Finance cares about profitability and resource allocation
                if len(numeric_cols) > 0:
                    value_col = numeric_cols[0]
                    below_avg = len(df[df[value_col] < df[value_col].mean()])
                    
                    if below_avg > len(df) / 2:
                        role_insights = "From a financial perspective, there's an opportunity to optimize resource allocation "
                        role_insights += f"since {below_avg} items are performing below average. Consider reviewing the ROI of lower-performing categories."
                    else:
                        role_insights = "From a financial perspective, the current distribution shows healthy performance across most categories, "
                        role_insights += "suggesting effective resource allocation."
                else:
                    role_insights = "From a financial perspective, further quantitative analysis would be beneficial to assess the profitability implications."
            
            else:
                # Generic role insights
                role_insights = f"Based on your role as {user_role}, these insights can help inform your specific business decisions."
        
        except Exception as e:
            role_insights = f"Additional insights tailored to your role as {user_role} would be valuable for decision-making."
        
        return role_insights