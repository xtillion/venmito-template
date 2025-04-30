/**
 * Transactions JavaScript for Venmito
 * 
 * This file handles the transactions page functionality, including:
 * - Loading and displaying transactions list
 * - Handling pagination
 * - Displaying transaction details in modals
 * - Filtering transactions by item, store, and price range
 * - Rendering charts for item and store data
 */

// Store current page state
const state = {
    currentPage: 1,
    perPage: 20,
    filters: {
      userId: null,
      item: null,
      store: null,
      minPrice: null,
      maxPrice: null
    },
    transactions: []
  };
  
  document.addEventListener('DOMContentLoaded', async () => {
    // Initialize charts with loading state
    initializeCharts();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial transactions data
    await loadTransactions();
    
    // Load chart data
    await loadChartData();
  });
  
  /**
   * Initialize charts with loading state
   */
  function initializeCharts() {
    // Create empty top items chart
    const topItemsCtx = document.getElementById('top-items-chart');
    if (topItemsCtx) {
      window.topItemsChart = new Chart(topItemsCtx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [{
            label: 'Revenue ($)',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading top items...'
            }
          },
          scales: {
            x: {
              beginAtZero: true
            }
          }
        }
      });
    }
    
    // Create empty top stores chart
    const topStoresCtx = document.getElementById('top-stores-chart');
    if (topStoresCtx) {
      window.topStoresChart = new Chart(topStoresCtx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [{
            label: 'Revenue ($)',
            data: [],
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading top stores...'
            }
          },
          scales: {
            x: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }
  
  /**
   * Set up event listeners for the page
   */
  function setupEventListeners() {
    // Filter button click
    document.getElementById('filter-btn')?.addEventListener('click', () => {
      // Get filter values
      const itemSearch = document.getElementById('item-search').value;
      const storeSearch = document.getElementById('store-search').value;
      const minPrice = document.getElementById('min-price').value;
      const maxPrice = document.getElementById('max-price').value;
      
      // Update state with filter values
      state.filters.item = itemSearch || null;
      state.filters.store = storeSearch || null;
      state.filters.minPrice = minPrice || null;
      state.filters.maxPrice = maxPrice || null;
      state.currentPage = 1; // Reset to first page when filtering
      
      // Reload transactions with new filters
      loadTransactions();
    });
  }
  
  /**
   * Load transactions data from API with pagination and filters
   */
  async function loadTransactions() {
    try {
      const transactionsTable = document.getElementById('transactions-table');
      const tableBody = transactionsTable?.querySelector('tbody');
      
      if (tableBody) {
        // Show loading state
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">Loading transactions...</td></tr>';
        
        // Fetch transactions data from API
        const response = await API.transactions.getTransactions(state.currentPage, state.perPage, state.filters);
        
        // Update state with transactions data
        state.transactions = response.data;
        
        // Render transactions table
        renderTransactionsTable(response.data);
        
        // Render pagination
        API.renderPagination(response.pagination, (page) => {
          state.currentPage = page;
          loadTransactions();
        }, 'transactions-pagination');
      }
    } catch (error) {
      console.error('Error loading transactions:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Load chart data from API
   */
  async function loadChartData() {
    try {
      // Load item summary data
      const itemSummary = await API.transactions.getItemSummary(10);
      updateTopItemsChart(itemSummary);
      
      // Load store summary data
      const storeSummary = await API.transactions.getStoreSummary(10);
      updateTopStoresChart(storeSummary);
    } catch (error) {
      console.error('Error loading chart data:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Update top items chart with data
   * 
   * @param {Array} data - Item summary data
   */
  function updateTopItemsChart(data) {
    if (!window.topItemsChart || !data || data.length === 0) return;
    
    // Format data for chart
    const sortedData = [...data].sort((a, b) => b.total_revenue - a.total_revenue).slice(0, 10);
    const labels = sortedData.map(item => item.item);
    const revenues = sortedData.map(item => item.total_revenue);
    
    // Update chart data
    window.topItemsChart.data.labels = labels;
    window.topItemsChart.data.datasets[0].data = revenues;
    window.topItemsChart.options.plugins.title.text = 'Top Items by Revenue';
    window.topItemsChart.update();
  }
  
  /**
   * Update top stores chart with data
   * 
   * @param {Array} data - Store summary data
   */
  function updateTopStoresChart(data) {
    if (!window.topStoresChart || !data || data.length === 0) return;
    
    // Format data for chart
    const sortedData = [...data].sort((a, b) => b.total_revenue - a.total_revenue).slice(0, 10);
    const labels = sortedData.map(store => store.store);
    const revenues = sortedData.map(store => store.total_revenue);
    
    // Update chart data
    window.topStoresChart.data.labels = labels;
    window.topStoresChart.data.datasets[0].data = revenues;
    window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
    window.topStoresChart.update();
  }
  
  /**
   * Render transactions table with the provided data
   * 
   * @param {Array} transactions - Transactions data from API
   */
  function renderTransactionsTable(transactions) {
    const tableBody = document.getElementById('transactions-table')?.querySelector('tbody');
    
    if (!tableBody) return;
    
    if (transactions.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No transactions found</td></tr>';
        return;
    }
    
    // Note: Transaction items are now separate, so we need to display something generic for the "Item" column
    // We'll update the item column to show a count instead of the specific item name
    tableBody.innerHTML = transactions.map(transaction => `
      <tr>
        <td>${transaction.transaction_id}</td>
        <td>${transaction.transaction_date ? API.formatDate(transaction.transaction_date) : 'N/A'}</td>
        <td>${transaction.items ? transaction.items.length + ' items' : 'Unknown'}</td>
        <td>${transaction.store}</td>
        <td>${API.formatCurrency(transaction.price)}</td>
        <td>${transaction.quantity || 'N/A'}</td>
        <td>
          <button class="btn btn-sm btn-primary view-transaction-btn" 
                  data-transaction-id="${transaction.transaction_id}" 
                  data-bs-toggle="modal" 
                  data-bs-target="#transactionModal">
            View
          </button>
        </td>
      </tr>
    `).join('');
    
    // Add event listeners for view buttons
    tableBody.querySelectorAll('.view-transaction-btn').forEach(button => {
      button.addEventListener('click', () => {
        const transactionId = button.dataset.transactionId;
        loadTransactionDetails(transactionId);
      });
    });
  }

  /**
   * Load transaction details for the modal
   * 
   * @param {string} transactionId - Transaction ID to load details for
   */
  async function loadTransactionDetails(transactionId) {
  try {
    // Get transaction details (now includes items array from our updated API method)
    const transaction = await API.transactions.getTransaction(transactionId);
    
    if (!transaction) {
      API.showError('Transaction not found');
      return;
    }
    
    // Get user details
    const user = await API.people.getUser(transaction.user_id);
    
    // Update modal with transaction details
    document.getElementById('transaction-id').textContent = transaction.transaction_id;
    document.getElementById('transaction-user').textContent = user ? `${user.first_name} ${user.last_name}` : `User #${transaction.user_id}`;
    document.getElementById('transaction-store').textContent = transaction.store;
    document.getElementById('transaction-price').textContent = transaction.price.toFixed(2);
    
    // Update items section - this assumes we add a new items section to the modal
    const itemsContainer = document.getElementById('transaction-items');
    if (itemsContainer) {
      if (transaction.items && transaction.items.length > 0) {
        // Generate HTML for each item
        const itemsHtml = transaction.items.map(item => `
          <tr>
            <td>${item.item}</td>
            <td>${item.quantity}</td>
            <td>${API.formatCurrency(item.price_per_item)}</td>
            <td>${API.formatCurrency(item.subtotal)}</td>
          </tr>
        `).join('');
        
        itemsContainer.innerHTML = `
          <table class="table table-sm">
            <thead>
              <tr>
                <th>Item</th>
                <th>Quantity</th>
                <th>Price/Item</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              ${itemsHtml}
            </tbody>
          </table>
        `;
      } else {
        itemsContainer.innerHTML = '<p class="text-muted">No items found for this transaction.</p>';
      }
    }
    
    // Update user details link
    document.getElementById('user-details-link').href = `/people/${transaction.user_id}`;
    
  } catch (error) {
    console.error('Error loading transaction details:', error);
    // Error handling is managed by the API utility
  }
}