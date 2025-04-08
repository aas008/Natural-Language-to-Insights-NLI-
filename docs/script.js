/**
 * Natural Language to Insights (NLI) - Main JavaScript
 * 
 * This script handles the chat interface, query processing, and result display
 * for the NLI web application.
 */

// Main application class
class NLIApp {
    constructor() {
      // DOM Elements
      this.elements = {
        queryInput: document.getElementById('query-input'),
        submitButton: document.getElementById('submit-query'),
        userRoleSelect: document.getElementById('user-role'),
        chatHistory: document.getElementById('chat-history'),
        exampleQueries: document.querySelectorAll('.example-query')
      };
  
      // Chat history
      this.conversationHistory = [];
  
      // Sample data for demo purposes (would be replaced by actual API calls)
      this.mockData = this.initializeMockData();
  
      // Initialize event listeners
      this.initEventListeners();
    }
  
    /**
     * Set up event listeners for user interactions
     */
    initEventListeners() {
      // Submit button click
      this.elements.submitButton.addEventListener('click', () => this.processQuery());
  
      // Enter key press in textarea
      this.elements.queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.processQuery();
        }
      });
  
      // Example query clicks
      this.elements.exampleQueries.forEach(query => {
        query.addEventListener('click', (e) => {
          e.preventDefault();
          this.elements.queryInput.value = query.textContent;
          this.processQuery();
        });
      });
    }
  
    /**
     * Process a user query
     */
    processQuery() {
      const query = this.elements.queryInput.value.trim();
      const userRole = this.elements.userRoleSelect.value;
      
      if (!query) {
        alert('Please enter a question.');
        return;
      }
      
      // Add user message to chat
      this.addMessageToChat('user', query);
      
      // Clear input
      this.elements.queryInput.value = '';
      
      // Add AI typing indicator
      const loadingMsgId = this.addMessageToChat(
        'ai', 
        '<div class="typing-indicator"><span></span><span></span><span></span></div>',
        true
      );
      
      // Simulate API request with timeout
      setTimeout(() => {
        // Remove loading message
        this.removeMessage(loadingMsgId);
        
        // Get query results
        const results = this.getQueryResults(query);
        
        if (results) {
          // Add AI response to chat
          this.addResponseToChat(results, userRole);
          
          // Add to conversation history
          this.conversationHistory.push({
            query: query,
            role: userRole,
            response: results
          });
        } else {
          // Add error message
          this.addMessageToChat(
            'ai', 
            "Sorry, I couldn't understand that query. Please try again or use one of the example questions."
          );
        }
        
        // Scroll to bottom of chat
        this.scrollToBottom();
      }, 1500); // Simulating API delay
    }
  
    /**
     * Add a message to the chat history
     */
    addMessageToChat(sender, content, isLoading = false) {
      const messageId = 'msg-' + Date.now();
      const messageDiv = document.createElement('div');
      messageDiv.className = sender === 'user' ? 'user-message' : 'ai-message';
      messageDiv.id = messageId;
      
      const avatar = document.createElement('div');
      avatar.className = 'avatar';
      avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
      
      const messageContent = document.createElement('div');
      messageContent.className = 'message-content';
      messageContent.innerHTML = content;
      
      if (!isLoading) {
        const messageTime = document.createElement('p');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageContent.appendChild(messageTime);
      }
      
      if (sender === 'user') {
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(avatar);
      } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
      }
      
      this.elements.chatHistory.appendChild(messageDiv);
      this.scrollToBottom();
      
      return messageId;
    }
  
    /**
     * Remove a message from chat by ID
     */
    removeMessage(messageId) {
      const message = document.getElementById(messageId);
      if (message) {
        message.remove();
      }
    }
  
    /**
     * Add AI response with visualization and data to chat
     */
    addResponseToChat(results, userRole) {
      // Create the AI response content
      let responseHTML = `<p>${results.insights}</p>`;
      
      // Add visualization
      responseHTML += `
        <div class="visualization-container">
          <img src="${results.chart}" alt="${results.visualization} chart" style="width:100%; max-width:600px;">
        </div>
      `;
      
      // Add tabs for additional information
      responseHTML += `
        <div class="query-result">
          <div class="result-tabs">
            <div class="result-tab active" data-tab="insights">Insights</div>
            <div class="result-tab" data-tab="data">Data</div>
            <div class="result-tab" data-tab="sql">SQL</div>
          </div>
          
          <div class="result-content active" data-content="insights">
            <h4>Key Points:</h4>
            <ul>
              ${results.keyPoints.map(point => `<li>${point}</li>`).join('')}
            </ul>
            <div class="role-insight">
              <p><strong>${userRole} Insight:</strong> ${results.roleInsights[userRole]}</p>
            </div>
          </div>
          
          <div class="result-content" data-content="data">
            <table>
              <thead>
                <tr>
                  ${Object.keys(results.data[0]).map(header => 
                    `<th>${this.formatHeader(header)}</th>`).join('')}
                </tr>
              </thead>
              <tbody>
                ${results.data.map(row => `
                  <tr>
                    ${Object.keys(row).map(key => `
                      <td>${typeof row[key] === 'number' && (key.includes('sales') || key.includes('revenue')) ? 
                        this.formatCurrency(row[key]) : 
                        row[key]}
                      </td>
                    `).join('')}
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
          
          <div class="result-content" data-content="sql">
            <pre>${results.sql}</pre>
          </div>
        </div>
      `;
      
      // Add to chat
      this.addMessageToChat('ai', responseHTML);
      
      // Add event listeners for tabs
      setTimeout(() => {
        const tabs = document.querySelectorAll('.result-tab');
        tabs.forEach(tab => {
          tab.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            // Remove active class from all tabs and contents
            document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.result-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.querySelector(`.result-content[data-content="${tabName}"]`).classList.add('active');
          });
        });
      }, 0);
    }
  
    /**
     * Scroll chat to bottom
     */
    scrollToBottom() {
      this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
    }
  
    /**
     * Get results for a query (in a real app, this would call an API)
     */
    getQueryResults(query) {
      // This is where you would normally make an API call to your backend
      // For the demo, we'll just match against keywords and return mock data
      
      query = query.toLowerCase();
      
      if (query.includes('region') && !query.includes('compare')) {
        return this.mockData.regions;
      } else if (query.includes('product') && (query.includes('top') || query.includes('revenue'))) {
        return this.mockData.products;
      } else if (query.includes('compare') || (query.includes('north') && query.includes('south'))) {
        return this.mockData.comparison;
      } else if (query.includes('category') || query.includes('distribution')) {
        return this.mockData.categories;
      }
      
      // Default to regions if no match
      return this.mockData.regions;
    }
  
    /**
     * Format header text (convert snake_case to Title Case)
     */
    formatHeader(header) {
      return header.split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    }
  
    /**
     * Format currency values
     */
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
      }).format(value);
    }
  
    /**
     * Initialize mock data for demo purposes
     */
    initializeMockData() {
      return {
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
    }
  }
  
  // Initialize the app when the DOM is fully loaded
  document.addEventListener('DOMContentLoaded', () => {
    const app = new NLIApp();
  });