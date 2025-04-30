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
  console.log('Transactions page initializing...');
  
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
  console.log('Initializing charts...');
  
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
  console.log('Setting up event listeners...');
  
  // Filter button click
  document.getElementById('filter-btn')?.addEventListener('click', () => {
    // Get filter values
    const itemSearch = document.getElementById('item-search')?.value;
    const storeSearch = document.getElementById('store-search')?.value;
    const minPrice = document.getElementById('min-price')?.value;
    const maxPrice = document.getElementById('max-price')?.value;
    
    // Update state with filter values
    state.filters.item = itemSearch || null;
    state.filters.store = storeSearch || null;
    state.filters.minPrice = minPrice || null;
    state.filters.maxPrice = maxPrice || null;
    state.currentPage = 1; // Reset to first page when filtering
    
    // Reload transactions with new filters
    loadTransactions();
  });
  
  // Add event listeners for pagination links
  const paginationLinks = document.querySelectorAll('#transactions-pagination .page-link');
  paginationLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = parseInt(e.target.dataset.page);
      if (!isNaN(page)) {
        state.currentPage = page;
        loadTransactions();
      }
    });
  });
}

/**
 * Load transactions data from API with pagination and filters
 */
async function loadTransactions() {
  console.log('Loading transactions...');
  try {
    const transactionsTable = document.getElementById('transactions-table');
    const tableBody = transactionsTable?.querySelector('tbody');
    
    if (tableBody) {
      // Show loading state
      tableBody.innerHTML = '<tr><td colspan="7" class="text-center">Loading transactions...</td></tr>';
      
      // Fetch transactions data from API
      const response = await window.API.transactions.getTransactions(state.currentPage, state.perPage, state.filters);
      
      // Update state with transactions data
      state.transactions = response.data || [];
      
      // Render transactions table
      renderTransactionsTable(state.transactions);
      
      // Render pagination
      if (response.pagination) {
        window.API.renderPagination(response.pagination, (page) => {
          state.currentPage = page;
          loadTransactions();
        }, 'transactions-pagination');
      }
    }
  } catch (error) {
    console.error('Error loading transactions:', error);
    const transactionsTable = document.getElementById('transactions-table');
    const tableBody = transactionsTable?.querySelector('tbody');
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Failed to load transactions. Please try again.</td></tr>';
    }
  }
}

/**
 * Load chart data from API
 */
async function loadChartData() {
  console.log('Loading chart data...');
  try {
    // Load item summary data
    const itemSummary = await window.API.transactions.getItemSummary(10);
    updateTopItemsChart(itemSummary);
    
    // Load store summary data
    const storeSummary = await window.API.transactions.getStoreSummary(10);
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
  console.log('Updating top items chart...');
  
  if (!window.topItemsChart || !data || data.length === 0) {
    console.warn('No chart or data available for top items');
    return;
  }
  
  // Format data for chart
  const sortedData = [...data]
    .sort((a, b) => {
      const revenueA = parseFloat(a.total_revenue) || 0;
      const revenueB = parseFloat(b.total_revenue) || 0;
      return revenueB - revenueA;
    })
    .slice(0, 10);
  
  const labels = sortedData.map(item => item.item);
  const revenues = sortedData.map(item => parseFloat(item.total_revenue) || 0);
  
  // Update chart data
  window.topItemsChart.data.labels = labels;
  window.topItemsChart.data.datasets[0].data = revenues;
  window.topItemsChart.options.plugins.title.text = 'Top Items by Revenue';
  window.topItemsChart.update();
  
  console.log('Top items chart updated');
}

/**
 * Update top stores chart with data
 * 
 * @param {Array} data - Store summary data
 */
function updateTopStoresChart(data) {
  console.log('Updating top stores chart...');
  
  if (!window.topStoresChart || !data || data.length === 0) {
    console.warn('No chart or data available for top stores');
    return;
  }
  
  // Format data for chart
  const sortedData = [...data]
    .sort((a, b) => {
      const revenueA = parseFloat(a.total_revenue) || 0;
      const revenueB = parseFloat(b.total_revenue) || 0;
      return revenueB - revenueA;
    })
    .slice(0, 10);
  
  const labels = sortedData.map(store => store.store);
  const revenues = sortedData.map(store => parseFloat(store.total_revenue) || 0);
  
  // Update chart data
  window.topStoresChart.data.labels = labels;
  window.topStoresChart.data.datasets[0].data = revenues;
  window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
  window.topStoresChart.update();
  
  console.log('Top stores chart updated');
}

/**
 * Render transactions table with the provided data
 * 
 * @param {Array} transactions - Transactions data from API
 */
function renderTransactionsTable(transactions) {
  console.log('Rendering transactions table...');
  
  const tableBody = document.getElementById('transactions-table')?.querySelector('tbody');
  
  if (!tableBody) {
    console.warn('No table body found for transactions');
    return;
  }
  
  if (!transactions || transactions.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No transactions found</td></tr>';
    return;
  }
  
  tableBody.innerHTML = transactions.map(transaction => {
    // Format item display based on item_count or first_item
    let itemDisplay = 'N/A';
    let quantityDisplay = 'N/A';
    
    // Handle different possible ways item info could be provided
    if (transaction.item_count > 0) {
      // New schema with item_count
      itemDisplay = transaction.item_count > 1 
        ? `${transaction.item_count} items` 
        : (transaction.first_item || 'Single item');
      
      quantityDisplay = transaction.total_quantity || 'N/A';
    } else if (transaction.items && transaction.items.length > 0) {
      // If we have items array directly
      itemDisplay = transaction.items.length > 1 
        ? `${transaction.items.length} items` 
        : transaction.items[0].item;
      
      quantityDisplay = transaction.items.reduce((sum, item) => sum + (parseInt(item.quantity) || 0), 0);
    } else if (transaction.item) {
      // Legacy schema with direct item field
      itemDisplay = transaction.item;
      quantityDisplay = transaction.quantity || 'N/A';
    }
    
    return `
      <tr>
        <td>${transaction.transaction_id}</td>
        <td>${transaction.transaction_date ? window.API.formatDate(transaction.transaction_date) : 'N/A'}</td>
        <td>${itemDisplay}</td>
        <td>${transaction.store || 'N/A'}</td>
        <td>${window.API.formatCurrency(transaction.price)}</td>
        <td>${quantityDisplay}</td>
        <td>
          <button class="btn btn-sm btn-primary view-transaction-btn" 
                  data-transaction-id="${transaction.transaction_id}" 
                  data-bs-toggle="modal" 
                  data-bs-target="#transactionModal">
            View
          </button>
        </td>
      </tr>
    `;
  }).join('');
  
  // Add event listeners for view buttons
  tableBody.querySelectorAll('.view-transaction-btn').forEach(button => {
    button.addEventListener('click', () => {
      const transactionId = button.dataset.transactionId;
      loadTransactionDetails(transactionId);
    });
  });
  
  console.log('Transactions table rendered with', transactions.length, 'rows');
}

/**
 * Load transaction details for the modal
 * 
 * @param {string} transactionId - Transaction ID to load details for
 */
async function loadTransactionDetails(transactionId) {
  console.log('Loading transaction details for', transactionId);
  
  try {
    // Show loading state in the modal
    const itemsContainer = document.getElementById('transaction-items');
    if (itemsContainer) {
      itemsContainer.innerHTML = 
        '<div class="text-center"><div class="spinner-border text-primary" role="status">' +
        '<span class="visually-hidden">Loading...</span></div><p class="mt-2">Loading items...</p></div>';
    }
    
    // Get complete transaction with items
    const transaction = await window.API.transactions.getTransactionWithItems(transactionId);
    
    if (!transaction) {
      console.error('Transaction not found');
      window.API.showError('Transaction not found');
      return;
    }
    
    console.log('Transaction details loaded:', transaction);
    
    // Get user details
    const user = await window.API.people.getUser(transaction.user_id);
    console.log('User details loaded:', user);
    
    // Update modal with transaction details
    document.getElementById('transaction-id').textContent = transaction.transaction_id;
    document.getElementById('transaction-user').textContent = user 
      ? `${user.first_name || ''} ${user.last_name || ''}`.trim() 
      : `User #${transaction.user_id}`;
    document.getElementById('transaction-store').textContent = transaction.store || 'N/A';
    document.getElementById('transaction-price').textContent = transaction.price.toFixed(2);
    
    // Format and display date
    const dateElement = document.getElementById('transaction-date');
    if (dateElement) {
      dateElement.textContent = transaction.transaction_date 
        ? window.API.formatDateTime(transaction.transaction_date) 
        : 'N/A';
    }
    
    // Update user details link
    const userLink = document.getElementById('user-details-link');
    if (userLink) {
      userLink.href = `/people/${transaction.user_id}`;
    }
    
    // Update items container
    if (itemsContainer) {
      if (transaction.items && transaction.items.length > 0) {
        // Generate HTML for each item
        const itemsHtml = transaction.items.map(item => `
          <tr>
            <td>${item.item || 'Unknown'}</td>
            <td>${item.quantity || 0}</td>
            <td>${window.API.formatCurrency(item.price_per_item || 0)}</td>
            <td>${window.API.formatCurrency(item.subtotal || (item.price_per_item * item.quantity) || 0)}</td>
          </tr>
        `).join('');
        
        // Create a table with the items
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
            <tfoot>
              <tr>
                <th colspan="3" class="text-end">Total:</th>
                <th>${window.API.formatCurrency(transaction.price)}</th>
              </tr>
            </tfoot>
          </table>
        `;
        
        // Add additional info if there's a discrepancy between items subtotal and transaction price
        if (transaction.itemsSubtotal && Math.abs(transaction.itemsSubtotal - transaction.price) > 0.01) {
          itemsContainer.innerHTML += `
            <div class="alert alert-info mt-2">
              <small>Note: There is a difference between the sum of item subtotals (${window.API.formatCurrency(transaction.itemsSubtotal)}) 
              and the transaction total (${window.API.formatCurrency(transaction.price)}). 
              This may be due to discounts, taxes, or other adjustments.</small>
            </div>
          `;
        }
      } else {
        itemsContainer.innerHTML = '<p class="text-muted">No items found for this transaction.</p>';
      }
    }
    
    console.log('Transaction details rendered successfully');
  } catch (error) {
    console.error('Error loading transaction details:', error);
    const itemsContainer = document.getElementById('transaction-items');
    if (itemsContainer) {
      itemsContainer.innerHTML = 
        '<div class="alert alert-danger">Failed to load transaction items. Please try again.</div>';
    }
  }
}