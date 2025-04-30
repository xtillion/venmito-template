/**
 * API Utilities for Venmito
 * 
 * This module provides functionality for interacting with the Venmito API,
 * including fetching data, error handling, and data formatting.
 */

// Create the API object in the global window scope
window.API = {
  /**
   * Base URL for all API requests
   */
  baseUrl: '/api',

  /**
   * Generic fetch function with error handling
   * 
   * @param {string} endpoint - API endpoint to fetch from
   * @param {Object} options - Fetch options (method, headers, body, etc.)
   * @param {Function} fallbackData - Function that returns fallback data in case of error
   * @returns {Promise<Object>} - The API response data
   */
  async fetch(endpoint, options = {}, fallbackData = null) {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Error fetching from ${url}:`, error);
      
      // Show a toast notification or alert
      this.showError(`Failed to load data from ${endpoint}`);
      
      // Return fallback data if provided
      if (fallbackData) {
        console.log('Using fallback data');
        return fallbackData();
      }
      
      return null;
    }
  },

  /**
   * Show an error message to the user
   * 
   * @param {string} message - Error message to display
   */
  showError(message) {
    // Simple error display - you can enhance this
    const errorContainer = document.createElement('div');
    errorContainer.className = 'alert alert-danger alert-dismissible fade show';
    errorContainer.innerHTML = `
      <strong>Error:</strong> ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
      container.insertBefore(errorContainer, container.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      errorContainer.remove();
    }, 5000);
  },

  /**
   * Format a number as currency
   * 
   * @param {number} amount - Amount to format
   * @returns {string} - Formatted currency string
   */
  formatCurrency(amount) {
    if (amount === null || amount === undefined) return '--';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(amount);
  },

  /**
   * Format a date string
   * 
   * @param {string} dateString - Date string to format
   * @returns {string} - Formatted date string
   */
  formatDate(dateString) {
    if (!dateString) return '--';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  },

  /**
   * Format a datetime string
   * 
   * @param {string} dateString - Datetime string to format
   * @returns {string} - Formatted datetime string
   */
  formatDateTime(dateString) {
    if (!dateString) return '--';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  },

  /**
   * Format a large number with abbreviations (K, M, B)
   * 
   * @param {number} num - Number to format
   * @returns {string} - Formatted number
   */
  formatLargeNumber(num) {
    if (num === null || num === undefined) return '--';
    
    if (num >= 1000000000) {
      return (num / 1000000000).toFixed(1) + 'B';
    } else if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    } else {
      return num.toString();
    }
  },

  /**
   * Generate chart colors
   * 
   * @param {number} count - Number of colors needed
   * @returns {Array<string>} - Array of color strings
   */
  generateChartColors(count) {
    const colors = [
      'rgba(54, 162, 235, 0.7)',   // Blue
      'rgba(255, 99, 132, 0.7)',    // Pink
      'rgba(75, 192, 192, 0.7)',    // Green
      'rgba(255, 159, 64, 0.7)',    // Orange
      'rgba(153, 102, 255, 0.7)',   // Purple
      'rgba(255, 205, 86, 0.7)',    // Yellow
      'rgba(201, 203, 207, 0.7)',   // Grey
      'rgba(255, 99, 71, 0.7)',     // Tomato
      'rgba(60, 179, 113, 0.7)',    // Medium Sea Green
      'rgba(106, 90, 205, 0.7)'     // Slate Blue
    ];
    
    if (count <= colors.length) {
      return colors.slice(0, count);
    }
    
    // If we need more colors than in our predefined list
    const result = [...colors];
    const neededExtras = count - colors.length;
    
    for (let i = 0; i < neededExtras; i++) {
      const r = Math.floor(Math.random() * 255);
      const g = Math.floor(Math.random() * 255);
      const b = Math.floor(Math.random() * 255);
      result.push(`rgba(${r}, ${g}, ${b}, 0.7)`);
    }
    
    return result;
  },

  /**
   * Generate pagination HTML
   * 
   * @param {Object} pagination - Pagination metadata from API
   * @param {Function} onPageChange - Callback when page changes
   * @param {string} elementId - ID of element to update
   */
  renderPagination(pagination, onPageChange, elementId) {
    const paginationElement = document.getElementById(elementId);
    if (!paginationElement) return;
    
    const { current_page, total_pages } = pagination;
    
    let html = '';
    
    // Previous button
    html += `<li class="page-item ${current_page === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" data-page="${current_page - 1}">Previous</a>
    </li>`;
    
    // Page numbers
    const maxVisiblePages = 5;
    let startPage = Math.max(1, current_page - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(total_pages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage < maxVisiblePages - 1) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    if (startPage > 1) {
      html += `<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>`;
      if (startPage > 2) {
        html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
      }
    }
    
    for (let i = startPage; i <= endPage; i++) {
      html += `<li class="page-item ${i === current_page ? 'active' : ''}">
        <a class="page-link" href="#" data-page="${i}">${i}</a>
      </li>`;
    }
    
    if (endPage < total_pages) {
      if (endPage < total_pages - 1) {
        html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
      }
      html += `<li class="page-item"><a class="page-link" href="#" data-page="${total_pages}">${total_pages}</a></li>`;
    }
    
    // Next button
    html += `<li class="page-item ${current_page === total_pages ? 'disabled' : ''}">
      <a class="page-link" href="#" data-page="${current_page + 1}">Next</a>
    </li>`;
    
    paginationElement.innerHTML = html;
    
    // Add event listeners
    paginationElement.querySelectorAll('.page-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = parseInt(e.target.dataset.page);
        if (page && page !== current_page && !e.target.parentElement.classList.contains('disabled')) {
          onPageChange(page);
        }
      });
    });
  },

  /**
   * People API endpoints
   */
  people: {
    /**
     * Get all users with pagination
     * 
     * @param {number} page - Page number
     * @param {number} perPage - Items per page
     * @param {string} search - Search term
     * @returns {Promise<Object>} - Users data
     */
    async getUsers(page = 1, perPage = 20, search = '') {
      const queryParams = new URLSearchParams({ page, per_page: perPage });
      if (search) queryParams.append('search', search);
      
      return window.API.fetch(`/people?${queryParams.toString()}`, {}, () => ({
        data: [],
        pagination: { total: 0, per_page: perPage, current_page: page, total_pages: 1 }
      }));
    },
    
    /**
     * Get a user by ID
     * 
     * @param {number} userId - User ID
     * @returns {Promise<Object>} - User data
     */
    async getUser(userId) {
      return window.API.fetch(`/people/${userId}`, {}, () => null);
    }
  },
  
  /**
   * Transfers API endpoints
   */
  transfers: {
    /**
     * Get all transfers with pagination
     * 
     * @param {number} page - Page number
     * @param {number} perPage - Items per page
     * @param {Object} filters - Filter options
     * @returns {Promise<Object>} - Transfers data
     */
    async getTransfers(page = 1, perPage = 20, filters = {}) {
      const queryParams = new URLSearchParams({ page, per_page: perPage });
      
      // Add filters if provided
      if (filters.userId) queryParams.append('user_id', filters.userId);
      if (filters.startDate) queryParams.append('start_date', filters.startDate);
      if (filters.endDate) queryParams.append('end_date', filters.endDate);
      
      return window.API.fetch(`/transfers?${queryParams.toString()}`, {}, () => ({
        data: [],
        pagination: { total: 0, per_page: perPage, current_page: page, total_pages: 1 }
      }));
    },
    
    /**
     * Get a transfer by ID
     * 
     * @param {number} transferId - Transfer ID
     * @returns {Promise<Object>} - Transfer data
     */
    async getTransfer(transferId) {
      return window.API.fetch(`/transfers/${transferId}`, {}, () => null);
    },
    
    /**
     * Get a user's transfer summary
     * 
     * @param {number} userId - User ID
     * @returns {Promise<Object>} - Transfer summary data
     */
    async getUserTransfersSummary(userId) {
      return window.API.fetch(`/transfers/user/${userId}/summary`, {}, () => ({
        user_id: userId,
        total_sent: 0,
        total_received: 0,
        net_transferred: 0,
        sent_count: 0,
        received_count: 0,
        transfer_count: 0
      }));
    },
    
    /**
     * Get a user's frequent contacts
     * 
     * @param {number} userId - User ID
     * @param {number} limit - Maximum number of contacts to return
     * @returns {Promise<Array>} - Frequent contacts data
     */
    async getUserFrequentContacts(userId, limit = 5) {
      return window.API.fetch(`/transfers/user/${userId}/contacts?limit=${limit}`, {}, () => []);
    }
  },
  
  /**
   * Transactions API endpoints
   */
  transactions: {
    /**
     * Get all transactions with pagination
     * 
     * @param {number} page - Page number
     * @param {number} perPage - Items per page
     * @param {Object} filters - Filter options
     * @returns {Promise<Object>} - Transactions data
     */
    async getTransactions(page = 1, perPage = 20, filters = {}) {
      const queryParams = new URLSearchParams({ page, per_page: perPage });
      
      // Add filters if provided
      if (filters.userId) queryParams.append('user_id', filters.userId);
      if (filters.item) queryParams.append('item', filters.item);
      if (filters.store) queryParams.append('store', filters.store);
      if (filters.minPrice) queryParams.append('min_price', filters.minPrice);
      if (filters.maxPrice) queryParams.append('max_price', filters.maxPrice);
      
      return window.API.fetch(`/transactions?${queryParams.toString()}`, {}, () => ({
        data: [],
        pagination: { total: 0, per_page: perPage, current_page: page, total_pages: 1 }
      }));
    },
    
    /**
     * Get a transaction by ID
     * 
     * @param {string} transactionId - Transaction ID
     * @returns {Promise<Object>} - Transaction data
     */
    async getTransaction(transactionId) {
      return window.API.fetch(`/transactions/${transactionId}`, {}, () => null);
    },

    /**
     * Get items for a specific transaction
     * 
     * @param {string} transactionId - Transaction ID
     * @returns {Promise<Array>} - Transaction items data
     */
    async getTransactionItems(transactionId) {
      return window.API.fetch(`/transactions/${transactionId}/items`, {}, () => []);
    },
    
    /**
     * Get items for a specific transaction
     * 
     * @param {string} transactionId - Transaction ID
     * @returns {Promise<Array>} - Transaction items data
     */
    async getTransactionWithItems(transactionId) {
      try {
        // Fetch both transaction and items in parallel
        const [transaction, items] = await Promise.all([
          this.getTransaction(transactionId),
          this.getTransactionItems(transactionId)
        ]);
        
        if (transaction) {
          // Attach items to transaction object
          transaction.items = items || [];
          
          // Calculate additional metrics
          if (items && items.length > 0) {
            transaction.totalItems = items.length;
            
            // Calculate total quantity across all items
            transaction.totalQuantity = items.reduce((sum, item) => {
              return sum + (parseInt(item.quantity) || 0);
            }, 0);
            
            // Calculate average price per item if not already present
            if (!transaction.averagePricePerItem && transaction.totalQuantity > 0) {
              transaction.averagePricePerItem = transaction.price / transaction.totalQuantity;
            }
            
            // Add an itemsSubtotal field to verify against transaction.price
            transaction.itemsSubtotal = items.reduce((sum, item) => {
              return sum + (parseFloat(item.subtotal) || 0);
            }, 0);
          } else {
            transaction.totalItems = 0;
            transaction.totalQuantity = 0;
            transaction.itemsSubtotal = 0;
          }
        }
        
        return transaction;
      } catch (error) {
        console.error(`Error fetching transaction ${transactionId} with items:`, error);
        return null;
      }
    },
    
    /**
     * Get multiple transactions with their items
     * 
     * @param {Array<string>} transactionIds - List of transaction IDs
     * @returns {Promise<Array<Object>>} - List of transactions with their items
     */
    async getTransactionsWithItems(transactionIds) {
      try {
        if (!transactionIds || !transactionIds.length) {
          return [];
        }
        
        // Fetch transactions first
        const transactions = await Promise.all(
          transactionIds.map(id => this.getTransaction(id))
        );
        
        // Fetch items for each transaction
        const transactionsWithItems = await Promise.all(
          transactions.filter(t => t) // Filter out any null transactions
            .map(async (transaction) => {
              try {
                const items = await this.getTransactionItems(transaction.transaction_id);
                
                // Attach items and calculate metrics
                transaction.items = items || [];
                
                if (items && items.length > 0) {
                  transaction.totalItems = items.length;
                  transaction.totalQuantity = items.reduce((sum, item) => sum + (parseInt(item.quantity) || 0), 0);
                  transaction.itemsSubtotal = items.reduce((sum, item) => sum + (parseFloat(item.subtotal) || 0), 0);
                } else {
                  transaction.totalItems = 0;
                  transaction.totalQuantity = 0;
                  transaction.itemsSubtotal = 0;
                }
                
                return transaction;
              } catch (e) {
                console.error(`Error fetching items for transaction ${transaction.transaction_id}:`, e);
                transaction.items = [];
                transaction.totalItems = 0;
                transaction.totalQuantity = 0;
                transaction.itemsSubtotal = 0;
                return transaction;
              }
            })
        );
        
        return transactionsWithItems;
      } catch (error) {
        console.error('Error fetching transactions with items:', error);
        return [];
      }
    },
  

    /**
     * Get a user's transaction summary
     * 
     * @param {number} userId - User ID
     * @returns {Promise<Object>} - Transaction summary data
     */
    async getUserTransactionsSummary(userId) {
      return window.API.fetch(`/transactions/user/${userId}/summary`, {}, () => ({
        user_id: userId,
        total_spent: 0,
        transaction_count: 0,
        favorite_store: null,
        favorite_item: null
      }));
    },
    
    /**
     * Get item summary data
     * 
     * @param {number} limit - Maximum number of items to return
     * @returns {Promise<Array>} - Item summary data
     */
    async getItemSummary(limit = 20) {
      return window.API.fetch(`/transactions/items/summary?limit=${limit}`, {}, () => []);
    },
    
    /**
     * Get store summary data
     * 
     * @param {number} limit - Maximum number of stores to return
     * @returns {Promise<Array>} - Store summary data
     */
    async getStoreSummary(limit = 20) {
      return window.API.fetch(`/transactions/stores/summary?limit=${limit}`, {}, () => []);
    },
  },
  
  /**
   * Analytics API endpoints
   */
  analytics: {
    /**
     * Get daily transactions summary
     * 
     * @param {number} days - Number of days to include
     * @returns {Promise<Array>} - Daily transactions data
     */
    async getDailyTransactionsSummary(days = 30) {
      return window.API.fetch(`/analytics/transactions/daily?days=${days}`, {}, () => []);
    },

    
    
    /**
     * Get daily transfers summary
     * 
     * @param {number} days - Number of days to include
     * @returns {Promise<Array>} - Daily transfers data
     */
    async getDailyTransfersSummary(days = 30) {
      return window.API.fetch(`/analytics/transfers/daily?days=${days}`, {}, () => []);
    },
    
    /**
     * Get top users by spending
     * 
     * @param {number} limit - Maximum number of users to return
     * @returns {Promise<Array>} - Top spending users data
     */
    async getTopUsersBySpending(limit = 10) {
      return window.API.fetch(`/analytics/users/top-spending?limit=${limit}`, {}, () => []);
    },
    
    /**
     * Get top users by transfer volume
     * 
     * @param {number} limit - Maximum number of users to return
     * @returns {Promise<Array>} - Top transfer users data
     */
    async getTopUsersByTransfers(limit = 10) {
      return window.API.fetch(`/analytics/users/top-transfers?limit=${limit}`, {}, () => []);
    },
    
    /**
     * Get popular items by month
     * 
     * @param {number} months - Number of months to include
     * @returns {Promise<Array>} - Popular items data
     */
    async getPopularItemsByMonth(months = 12) {
      return window.API.fetch(`/analytics/items/monthly-popular?months=${months}`, {}, () => []);
    },
    
    /**
     * Get user spending distribution
     * 
     * @returns {Promise<Array>} - Spending distribution data
     */
    async getUserSpendingDistribution() {
      return window.API.fetch('/analytics/users/spending-distribution', {}, () => []);
    },
    
    /**
     * Get geographic spending summary
     * 
     * @returns {Promise<Array>} - Geographic spending data
     */
    async getGeographicSpendingSummary() {
      return window.API.fetch('/analytics/geographic/spending', {}, () => []);
    },
    
    /**
     * Get transfer amount distribution
     * 
     * @returns {Promise<Array>} - Transfer amount distribution data
     */
    async getTransferAmountDistribution() {
      return window.API.fetch('/analytics/transfers/amount-distribution', {}, () => []);
    },
    
    /**
   * Get dashboard totals
   * 
   * @returns {Promise<Object>} - Dashboard totals data
   */
  async getDashboardTotals() {
    return window.API.fetch('/analytics/dashboard-totals', {}, () => ({
        total_revenue: 0,
        total_transactions: 0,
        average_transaction_value: 0,
        unique_items_sold: 0,
        top_selling_item: 'N/A',
        top_item_revenue: 0,
        top_item_sales: 0
    }));
  },
  /**
   * Get top items
   * 
   * @param {number} limit - Maximum number of items to return (default 5)
   * @param {string} orderBy - Metric to order by ('revenue', 'sales', 'transactions')
   * @returns {Promise<Array>} - Top items data
   */
  async getTopItems(limit = 5, orderBy = 'revenue') {
    return window.API.fetch(
        `/analytics/top-items?limit=${limit}&order_by=${orderBy}`, 
        {}, 
        () => []
    );
  },

    /**
     * Get complete analytics dashboard data
     * 
     * @returns {Promise<Object>} - Dashboard data
     */
    async getDashboard() {
      return window.API.fetch('/analytics/dashboard', {}, () => ({
        top_users_by_spending: [],
        top_users_by_transfers: [],
        spending_distribution: [],
        transfer_distribution: [],
        daily_transactions: [],
        daily_transfers: []
      }));
    },
  
    /**
     * Get top transactions by amount
     * 
     * @param {number} limit - Maximum number of transactions to return
     * @returns {Promise<Array>} - Top transactions by amount
     */
      async getTopTransactions(limit = 5) {
        try {
          // Try the analytics endpoint first
          const transactions = await window.API.fetch(`/analytics/top-transactions?limit=${limit}`, {}, () => null);
          
          if (transactions) {
            return transactions;
          }
          
          // Fallback to getting all transactions and sorting manually
          const response = await this.getTransactions(1, 100);
          if (response && response.data && Array.isArray(response.data)) {
            // Sort by price and get top X
            return response.data
              .filter(tx => tx && tx.price !== undefined && tx.price !== null)
              .sort((a, b) => {
                const priceA = typeof a.price === 'string' ? parseFloat(a.price) : a.price;
                const priceB = typeof b.price === 'string' ? parseFloat(b.price) : b.price;
                return priceB - priceA;
              })
              .slice(0, limit);
          }
          
          return [];
        } catch (error) {
          console.error('Error getting top transactions:', error);
          return [];
        }
      }
  }
  };