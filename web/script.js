document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('query-input');
    const submitButton = document.getElementById('submit-query');
    const userRoleSelect = document.getElementById('user-role');
    const loadingIndicator = document.getElementById('loading');
    const resultsContainer = document.getElementById('results-container');
    const sqlOutput = document.getElementById('sql-output');
    const visualizationOutput = document.getElementById('visualization-output');
    const chartImage = document.getElementById('chart-image');
    const insightsOutput = document.getElementById('insights-output');
    const keyPointsOutput = document.getElementById('key-points');
    const roleInsightsOutput = document.getElementById('role-insights');
    const dataOutput = document.getElementById('data-output');
    const exampleQueries = document.querySelectorAll('.example-query');
    
    // For demo purposes, we'll use mockData
    let mockData = {
        // Sample data that would come from your backend
        regions: {
            sql: "SELECT region, SUM(sales_amount) as total_sales FROM sales GROUP BY region ORDER BY total_sales DESC",
            visualization: "bar",
            chart: "https://via.placeholder.com/600x400?text=Region+Sales+Chart",
            insights: "Analysis shows that North leads with $123,036.52 (28.2% of total), while West has the lowest value at $85,157.17. 2 out of 4 regions perform above the average of $108,907.54.",
            keyPoints: [
                "Total sales: $435,630.16",
                "Average sales per region: $108,907.54",
                "Top performer: North with $123,036.52",
                "Bottom performer: West with $85,157.17"
            ],
            roleInsights: {
                "Sales Manager": "As a Sales Manager, focus on replicating the success in North across other regions to maximize overall performance.",
                "Executive": "From an executive perspective, this data suggests a balanced distribution that aligns with the company's diversification goals.",
                "Finance": "From a financial perspective, there's an opportunity to optimize resource allocation in the West region to improve overall performance.",
                "Analyst": "The data indicates regional performance differences that warrant further analysis into contributing factors."
            },
            data: [
                { region: "North", total_sales: 123036.52 },
                { region: "South", total_sales: 134364.82 },
                { region: "East", total_sales: 93071.65 },
                { region: "West", total_sales: 85157.17 }
            ]
        },
        products: {
            sql: "SELECT product_name, SUM(sales_amount) as total_revenue FROM sales GROUP BY product_name ORDER BY total_revenue DESC LIMIT 5",
            visualization: "bar",
            chart: "https://via.placeholder.com/600x400?text=Product+Revenue+Chart",
            insights: "The top product, Laptop Pro, generates $148,515.25 (34.1% of total revenue), significantly ahead of other products. There's a 62.7% gap between the top and bottom performers in the top 5.",
            keyPoints: [
                "Top revenue generator: Laptop Pro with $148,515.25",
                "Second best performer: Smartphone X with $112,546.80",
                "Wide performance gap between products"
            ],
            roleInsights: {
                "Sales Manager": "As a Sales Manager, consider expanding the marketing efforts for Laptop Pro given its strong performance, while developing strategies to boost Monitor sales.",
                "Executive": "The product revenue distribution shows a healthy primary product (Laptop Pro) with supporting products creating a diversified portfolio.",
                "Finance": "Consider reviewing the pricing and margin strategy for the Monitor line to improve its revenue contribution.",
                "Analyst": "A deeper analysis of product attributes and marketing strategies could reveal why certain products outperform others."
            },
            data: [
                { product_name: "Laptop Pro", total_revenue: 148515.25 },
                { product_name: "Smartphone X", total_revenue: 112546.80 },
                { product_name: "Tablet Y", total_revenue: 97089.15 },
                { product_name: "Desktop Z", total_revenue: 63124.30 },
                { product_name: "Monitor", total_revenue: 55312.40 }
            ]
        },
        comparison: {
            sql: "SELECT region, SUM(sales_amount) as total_sales FROM sales WHERE region IN ('North', 'South') GROUP BY region ORDER BY total_sales DESC",
            visualization: "bar",
            chart: "https://via.placeholder.com/600x400?text=North+vs+South+Comparison",
            insights: "South region leads with $134,364.82 in sales, outperforming North by $11,328.30 (9.2% higher). Together they account for 59.1% of total company sales.",
            keyPoints: [
                "South region: $134,364.82",
                "North region: $123,036.52",
                "Difference: $11,328.30 (9.2%)"
            ],
            roleInsights: {
                "Sales Manager": "As Sales Manager, investigate what strategies are working well in the South region that could be applied to North to close the performance gap.",
                "Executive": "The relatively small difference between these major regions indicates balanced regional performance, which reduces geographic risk.",
                "Finance": "The 9.2% performance difference between regions suggests potential for optimization in resource allocation to the North region.",
                "Analyst": "Further analysis of demographic differences and regional buying patterns could explain the performance variation."
            },
            data: [
                { region: "South", total_sales: 134364.82 },
                { region: "North", total_sales: 123036.52 }
            ]
        },
        categories: {
            sql: "SELECT product_category, SUM(sales_amount) as total_sales FROM sales GROUP BY product_category",
            visualization: "pie",
            chart: "https://via.placeholder.com/600x400?text=Category+Distribution+Chart",
            insights: "Electronics dominates with 76.4% ($332,869.35) of total sales, while Accessories accounts for 23.6% ($102,760.81). This indicates a strong concentration in the Electronics category.",
            keyPoints: [
                "Electronics: $332,869.35 (76.4%)",
                "Accessories: $102,760.81 (23.6%)",
                "High concentration in Electronics category"
            ],
            roleInsights: {
                "Sales Manager": "As a Sales Manager, while Electronics drives most sales, consider growth opportunities in Accessories which may have higher margins or cross-selling potential.",
                "Executive": "The heavy concentration in Electronics represents both a strength and potential risk. Consider strategic initiatives to grow the Accessories segment for greater balance.",
                "Finance": "Given the sales distribution, ensure that resource allocation and inventory management align with the dominance of the Electronics category.",
                "Analyst": "Further analysis of profit margins between categories would provide valuable context to this sales distribution."
            },
            data: [
                { product_category: "Electronics", total_sales: 332869.35 },
                { product_category: "Accessories", total_sales: 102760.81 }
            ]
        }
    };
    
    // Event listener for submit button
    submitButton.addEventListener('click', function() {
        processQuery();
    });
    
    // Event listener for Enter key in textarea
    queryInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            processQuery();
        }
    });
    
    // Event listeners for example queries
    exampleQueries.forEach(query => {
        query.addEventListener('click', function(e) {
            e.preventDefault();
            queryInput.value = this.textContent;
            processQuery();
        });
    });
    
    function processQuery() {
        const query = queryInput.value.trim();
        
        if (!query) {
            alert('Please enter a question.');
            return;
        }
        
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        resultsContainer.style.display = 'none';
        
        // Simulate API request with timeout
        setTimeout(() => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            
            // Process the query and get results
            const results = getQueryResults(query);
            
            if (results) {
                // Display results
                displayResults(results);
            } else {
                alert('Sorry, I could not understand that query. Please try again or use one of the example questions.');
            }
        }, 1500); // Simulating API delay
    }
    
    function getQueryResults(query) {
        // This is where you would normally make an API call to your backend
        // For the demo, we'll just match against keywords and return mock data
        
        query = query.toLowerCase();
        
        if (query.includes('region') && !query.includes('compare')) {
            return mockData.regions;
        } else if (query.includes('product') && (query.includes('top') || query.includes('revenue'))) {
            return mockData.products;
        } else if (query.includes('compare') || (query.includes('north') && query.includes('south'))) {
            return mockData.comparison;
        } else if (query.includes('category') || query.includes('distribution')) {
            return mockData.categories;
        }
        
        // Default to regions if no match
        return mockData.regions;
    }
    
    function displayResults(results) {
        // Display SQL
        sqlOutput.textContent = results.sql;
        
        // Display visualization
        chartImage.src = results.chart;
        chartImage.alt = `${results.visualization} chart of the data`;
        
        // Display insights
        insightsOutput.textContent = results.insights;
        
        // Display key points
        let keyPointsHTML = '<ul>';
        results.keyPoints.forEach(point => {
            keyPointsHTML += `<li>${point}</li>`;
        });
        keyPointsHTML += '</ul>';
        keyPointsOutput.innerHTML = keyPointsHTML;
        
        // Display role-specific insights
        const userRole = userRoleSelect.value;
        roleInsightsOutput.textContent = results.roleInsights[userRole] || '';
        
        // Display data table
        let tableHTML = '<table><thead><tr>';
        
        // Get column headers from the first data item
        const headers = Object.keys(results.data[0]);
        headers.forEach(header => {
            tableHTML += `<th>${formatHeader(header)}</th>`;
        });
        
        tableHTML += '</tr></thead><tbody>';
        
        // Add data rows
        results.data.forEach(row => {
            tableHTML += '<tr>';
            headers.forEach(header => {
                let cellValue = row[header];
                // Format numbers if needed
                if (typeof cellValue === 'number') {
                    if (header.includes('sales') || header.includes('revenue')) {
                        cellValue = formatCurrency(cellValue);
                    } else {
                        cellValue = cellValue.toLocaleString();
                    }
                }
                tableHTML += `<td>${cellValue}</td>`;
            });
            tableHTML += '</tr>';
        });
        
        tableHTML += '</tbody></table>';
        dataOutput.innerHTML = tableHTML;
        
        // Show results container
        resultsContainer.style.display = 'block';
    }
    
    function formatHeader(header) {
        // Convert snake_case to Title Case
        return header.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    
    function formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(value);
    }
});