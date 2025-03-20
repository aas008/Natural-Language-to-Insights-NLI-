# Natural-Language-to-Insights-NLI-Scope of Work (SOW)
Project Title:
Natural Language to Insights (NLI) – Business Intelligence through Conversational AI
Prepared For:
Executive Leadership & Business Teams
Prepared By:
Aanya Sharma
Date:
3/12/25
1. Project Overview
This project aims to empower business users to retrieve insights from enterprise data using natural language queries (English). By leveraging a Large Language Model (LLM), the system will translate user prompts into SQL queries, extract the relevant data, and present it in the form of visualizations (graphs, tables, dashboards) through Power BI or similar tools.

The system is role-aware, ensuring that outputs are tailored to the user's business function, with insights presented in formats most useful to them.

2. Goals and Objectives
• Allow users to ask questions in plain English to access business data.
• Automatically generate SQL queries from natural language prompts.
• Provide visual and written insights through Power BI dashboards.
• Support role-based personalization to adapt outputs depending on the user (Sales, Finance, Operations, etc.).
• Enhance executive decision-making through simplified, on-demand analytics.


3. Process Flow
• User Input: User enters a natural language prompt specifying the analysis.
• Persona Detection: System captures the user's role/persona to customize output (e.g., Salesperson, Executive).
• Query Generation: LLM interprets the prompt and generates a corresponding SQL query.
• Data Retrieval: Query is executed against the appropriate database/table.
• Visualization Creation: Results are presented via graphs, tables, or dashboards with proper titles and annotations.
• Insight Generation: The system provides a brief narrative analysis explaining the key insights from the visualization.
• Source Linking: Visuals and tables include links to the underlying data for further exploration.

4. Sample Use Cases
Role: Salesperson
Prompt: Show me a graph of sales over the last 5 years.
Output: Line graph titled '5-Year Sales Trend' with a short performance analysis.


Role: Executive
Prompt: Analyze quarterly revenue and give key insights.
Output: Bar chart of revenue by quarter with a summary of trends.


Role: Finance
Prompt: Provide a table of top 10 customers by revenue.
Output: Table listing customers, revenue, and data link.


Role: Salesperson
Prompt: Compare this year's sales to last year's in the North region.
Output: Side-by-side bar chart with comparison and insights.


5. Supported Data Sources
Current Support:
• Database Tables
• CSV, Excel

Future Support:
• PDFs (Single/Multiple)
• Images (Scanned Reports, Charts)
• Unstructured Text
• Multilingual Queries (Hindi, Hinglish)
6. Deliverables
• Interactive interface for natural language queries.
• Automatic SQL generation and execution.
• Dynamic graph/table creation in Power BI.
• Narrative insights summarizing data trends.
• Role-based output customization.
• Linkage to source data for further exploration.
7. Future Roadmap
• Phase 1: Ingest and analyze unstructured files like PDFs and images.
• Phase 2: Enable multilingual querying (English ↔ Hindi ↔ Hinglish).
• Phase 3: Support complex queries with multiple filters, joins, and conditions.
• Phase 4: Generate multiple graphs and full dashboards from a single prompt.
• Phase 5: Auto-summarize attached documents alongside visual insights.
• Phase 6: Integration with external communication tools (e.g., Slack, Teams) for conversational data insights.
8. Example Scenario (Salesperson Persona)
Prompt:
Show me last 5 years of sales in a graph.

Output:
- Line graph titled 'Sales from 2019 to 2024'.
- Narrative insight: 'Sales have steadily increased with a notable 15% growth in 2023.'
- Link to source data for further exploration.
User Flow:  


9. Key Benefits
• Simplifies data access for non-technical users.
• Reduces dependency on specialized analysts for routine reporting.
• Provides instant insights customized to business roles.
• Enhances decision-making with easy-to-understand visuals and summaries.
• Scales across departments through flexible file support and query handling.
10. Next Steps
• Finalize technical requirements and data sources.
• Begin development of natural language interface.
• Plan phased rollout, starting with Sales persona.
• Gather feedback to inform future feature development.


