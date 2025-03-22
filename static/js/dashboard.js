/**
 * Dashboard JavaScript for Venmito
 * 
 * This file handles the dashboard functionality, including:
 * - Loading and displaying summary statistics
 * - Rendering charts for item and store data
 * - Displaying top transactions and transfers
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Dashboard: DOM loaded, initializing...');
  
  // Update the "Recent Transactions" title to "Top Transactions"
  updateTransactionTitle();
  
  // Initialize charts with loading state
  initializeCharts();
  
  // Load dashboard data
  await loadDashboardData();
});

/**
 * Update the transaction section title from "Recent" to "Top"
 */
function updateTransactionTitle() {
  const transactionHeader = document.querySelector('#recent-transactions-table')?.closest('.card')?.querySelector('.card-header');
  if (transactionHeader) {
    transactionHeader.textContent = 'Top Transactions by Amount';
  }
}

/**
 * Initialize charts with loading state
 */
function initializeCharts() {
  console.log('Dashboard: Initializing charts');
  // Create top items chart
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
  } else {
    console.warn('Dashboard: Could not find top-items-chart element');
  }
  
  // Create top stores chart
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
  } else {
    console.warn('Dashboard: Could not find top-stores-chart element');
  }
}

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
  console.log('Dashboard: Loading dashboard data...');
  try {
    // Set default values for summary cards
    setDefaultSummaryValues();
    
    // Try to get analytics dashboard data, with error handling
    try {
      const dashboardData = await window.API.analytics.getDashboard();
      console.log('Dashboard API response:', dashboardData);
      
      // Update summary cards if data exists
      if (dashboardData) {
        updateSummaryCards(dashboardData);
      }
    } catch (err) {
      console.error('Failed to load dashboard analytics data:', err);
      // Continue with other data loading attempts
    }
    
    // Load additional data
    await loadAdditionalData();
  } catch (error) {
    console.error('Error loading dashboard data:', error);
    // Still try to load any data we can
    try {
      await loadTransactionsData();
    } catch (e) {
      console.error('Failed to load transactions as fallback:', e);
    }
  }
}

/**
 * Set default values for summary cards
 */
function setDefaultSummaryValues() {
  // Set placeholder values
  document.getElementById('total-users').textContent = '0';
  document.getElementById('total-transfers').textContent = '0';
  document.getElementById('total-transactions').textContent = '0';
  document.getElementById('total-revenue').textContent = '$0.00';
}

/**
 * Format number with commas for thousands
 */
function formatNumber(number) {
  return new Intl.NumberFormat().format(number);
}

/**
 * Format currency amount
 */
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

// Add these utility functions to the window object for broader use
window.venmito = {
  formatNumber,
  formatCurrency
};

/**
 * Load additional data for charts and tables
 */
async function loadAdditionalData() {
  console.log('Dashboard: Loading additional data for charts...');
  
  // Create a promise array to load data in parallel
  const dataPromises = [
    loadTransactionsData(),
    loadItemsData(),
    loadStoresData(),
    loadTransfersData()
  ];
  
  // Execute all promises, but don't fail if one fails
  const results = await Promise.allSettled(dataPromises);
  
  // Check results
  results.forEach((result, index) => {
    if (result.status === 'rejected') {
      console.error(`Data loading promise ${index} failed:`, result.reason);
    }
  });
}

/**
 * Load transactions data
 */
async function loadTransactionsData() {
  console.log('Dashboard: Loading transactions data...');
  try {
    const response = await window.API.transactions.getTransactions(1, 100);
    console.log('Transactions data:', response);
    
    // Extract transactions depending on response format
    let transactions = [];
    if (response && response.data && Array.isArray(response.data)) {
      transactions = response.data;
    } else if (Array.isArray(response)) {
      transactions = response;
    }
    
    // Update transaction count and revenue
    updateTransactionCount(transactions);
    
    // Update transactions table
    updateTransactionsTable(transactions);
    
    return transactions;
  } catch (error) {
    console.error('Error loading transactions:', error);
    handleTableLoadError('recent-transactions-table');
    throw error;
  }
}

/**
 * Load items data
 */
async function loadItemsData() {
  console.log('Dashboard: Loading items data...');
  try {
    const itemSummary = await window.API.transactions.getItemSummary(10);
    console.log('Item summary data:', itemSummary);
    updateTopItemsChart(itemSummary);
    return itemSummary;
  } catch (error) {
    console.error('Error loading items data:', error);
    // Update chart with error state
    if (window.topItemsChart) {
      window.topItemsChart.data.labels = ['Error loading data'];
      window.topItemsChart.data.datasets[0].data = [0];
      window.topItemsChart.options.plugins.title.text = 'Failed to load item data';
      window.topItemsChart.update();
    }
    throw error;
  }
}

/**
 * Load stores data
 */
async function loadStoresData() {
  console.log('Dashboard: Loading stores data...');
  try {
    const storeSummary = await window.API.transactions.getStoreSummary(10);
    console.log('Store summary data:', storeSummary);
    updateTopStoresChart(storeSummary);
    return storeSummary;
  } catch (error) {
    console.error('Error loading stores data:', error);
    // Update chart with error state
    if (window.topStoresChart) {
      window.topStoresChart.data.labels = ['Error loading data'];
      window.topStoresChart.data.datasets[0].data = [0];
      window.topStoresChart.options.plugins.title.text = 'Failed to load store data';
      window.topStoresChart.update();
    }
    throw error;
  }
}

/**
 * Load transfers data
 */
async function loadTransfersData() {
  console.log('Dashboard: Loading transfers data...');
  try {
    const transfers = await window.API.transfers.getTransfers(1, 10);
    console.log('Transfers data:', transfers);
    
    // Extract transfers depending on response format
    let transfersData = [];
    if (transfers && transfers.data && Array.isArray(transfers.data)) {
      transfersData = transfers.data;
    } else if (Array.isArray(transfers)) {
      transfersData = transfers;
    }
    
    // Update transfers count and table
    updateTransfersCount(transfersData);
    updateTransfersTable(transfersData);
    
    return transfersData;
  } catch (error) {
    console.error('Error loading transfers data:', error);
    handleTableLoadError('recent-transfers-table');
    throw error;
  }
}

/**
 * Update transaction count based on fetched data
 */ 
function updateTransactionCount(transactionsData) {
  let totalTransactions = 0;
  let totalRevenue = 0;
  
  // Check if we have transaction data
  if (Array.isArray(transactionsData)) {
    totalTransactions = transactionsData.length;
    
    // Calculate total revenue
    transactionsData.forEach(transaction => {
      if (transaction.price) {
        const price = typeof transaction.price === 'string' ? 
          parseFloat(transaction.price) : transaction.price;
        totalRevenue += isNaN(price) ? 0 : price;
      }
    });
  }
  
  console.log(`Dashboard: Updated transaction count: ${totalTransactions}, revenue: ${totalRevenue}`);
  
  // Update the UI
  document.getElementById('total-transactions').textContent = formatNumber(totalTransactions);
  document.getElementById('total-revenue').textContent = formatCurrency(totalRevenue);
}

/**
 * Update transfers count based on fetched data
 */
function updateTransfersCount(transfersData) {
  let totalTransfers = 0;
  
  // Check if we have transfer data
  if (Array.isArray(transfersData)) {
    totalTransfers = transfersData.length;
  }
  
  console.log(`Dashboard: Updated transfers count: ${totalTransfers}`);
  
  // Update the UI - only if not already set by the dashboard data
  const currentValue = document.getElementById('total-transfers').textContent;
  if (currentValue === '0' || currentValue === '--') {
    document.getElementById('total-transfers').textContent = formatNumber(totalTransfers);
  }
}

/**
 * Update summary cards with dashboard data
 */
function updateSummaryCards(dashboardData) {
  console.log('Dashboard: Updating summary cards with data:', dashboardData);
  
  // Extract data from the dashboard response
  let totalUsers = 0;
  let totalTransfers = 0;
  
  // Get user count from spending distribution
  if (dashboardData.spending_distribution && Array.isArray(dashboardData.spending_distribution)) {
    dashboardData.spending_distribution.forEach(range => {
      if (range.user_count) {
        totalUsers += parseInt(range.user_count) || 0;
      }
    });
    console.log(`Dashboard: User count from spending distribution: ${totalUsers}`);
  }
  
  // Get transfer count from transfer distribution
  if (dashboardData.transfer_distribution && Array.isArray(dashboardData.transfer_distribution)) {
    let transferAmount = 0;
    
    dashboardData.transfer_distribution.forEach(range => {
      if (range.transfer_count) {
        totalTransfers += parseInt(range.transfer_count) || 0;
      }
      if (range.total_amount) {
        transferAmount += parseFloat(range.total_amount) || 0;
      }
    });
    console.log(`Dashboard: Transfer count: ${totalTransfers}, amount: ${transferAmount}`);
  }
  
  // Only update if we have data
  if (totalUsers > 0) {
    document.getElementById('total-users').textContent = formatNumber(totalUsers);
  }
  
  if (totalTransfers > 0) {
    document.getElementById('total-transfers').textContent = formatNumber(totalTransfers);
  }
  
  // Transactions and revenue will be updated in updateTransactionCount
  
  console.log('Dashboard: Summary cards updated (users and transfers)');
}

/**
 * Handle error when loading table data
 */
function handleTableLoadError(tableId) {
  const tableBody = document.getElementById(tableId)?.querySelector('tbody');
  if (tableBody) {
    tableBody.innerHTML = '<tr><td colspan="4" class="text-center">Failed to load data</td></tr>';
  }
}

/**
 * Update transactions table with data
 */
function updateTransactionsTable(transactions) {
  console.log('Dashboard: Updating transactions table');
  
  const transactionsBody = document.getElementById('recent-transactions-table')?.querySelector('tbody');
  if (!transactionsBody) {
    console.warn('Dashboard: Could not find transactions table body');
    return;
  }
  
  if (!Array.isArray(transactions) || transactions.length === 0) {
    transactionsBody.innerHTML = '<tr><td colspan="4" class="text-center">No transactions available</td></tr>';
    return;
  }
  
  // Sort by price (highest first)
  const sortedTransactions = [...transactions].sort((a, b) => {
    const priceA = typeof a.price === 'string' ? parseFloat(a.price) : (a.price || 0);
    const priceB = typeof b.price === 'string' ? parseFloat(b.price) : (b.price || 0);
    return priceB - priceA;
  });
  
  // Take top 5
  const topTransactions = sortedTransactions.slice(0, 5);
  
  // Display transactions
  transactionsBody.innerHTML = topTransactions.map(transaction => `
    <tr>
      <td>${transaction.transaction_id || 'N/A'}</td>
      <td>${transaction.item || 'N/A'}</td>
      <td>${transaction.store || 'N/A'}</td>
      <td>${transaction.price ? formatCurrency(transaction.price) : 'N/A'}</td>
    </tr>
  `).join('');
  
  console.log('Dashboard: Transactions table updated');
}

/**
 * Update transfers table with data
 */
function updateTransfersTable(transfers) {
  console.log('Dashboard: Updating transfers table');
  
  const transfersBody = document.getElementById('recent-transfers-table')?.querySelector('tbody');
  if (!transfersBody) {
    console.warn('Dashboard: Could not find transfers table body');
    return;
  }
  
  if (!Array.isArray(transfers) || transfers.length === 0) {
    transfersBody.innerHTML = '<tr><td colspan="4" class="text-center">No transfers available</td></tr>';
    return;
  }
  
  // Sort by amount (highest first)
  const sortedTransfers = [...transfers].sort((a, b) => {
    const amountA = typeof a.amount === 'string' ? parseFloat(a.amount) : (a.amount || 0);
    const amountB = typeof b.amount === 'string' ? parseFloat(b.amount) : (b.amount || 0);
    return amountB - amountA;
  });
  
  // Take top 5
  const topTransfers = sortedTransfers.slice(0, 5);
  
  // Display transfers
  transfersBody.innerHTML = topTransfers.map(transfer => `
    <tr>
      <td>${transfer.transfer_id || 'N/A'}</td>
      <td>${getSenderName(transfer)}</td>
      <td>${getRecipientName(transfer)}</td>
      <td>${transfer.amount ? formatCurrency(transfer.amount) : 'N/A'}</td>
    </tr>
  `).join('');
  
  console.log('Dashboard: Transfers table updated');
}

/**
 * Get sender name from transfer object
 */
function getSenderName(transfer) {
  if (transfer.sender_name) {
    return transfer.sender_name;
  }
  if (transfer.sender && transfer.sender.first_name) {
    return `${transfer.sender.first_name} ${transfer.sender.last_name || ''}`;
  }
  return transfer.sender_id ? `User #${transfer.sender_id}` : 'N/A';
}

/**
 * Get recipient name from transfer object
 */
function getRecipientName(transfer) {
  if (transfer.recipient_name) {
    return transfer.recipient_name;
  }
  if (transfer.recipient && transfer.recipient.first_name) {
    return `${transfer.recipient.first_name} ${transfer.recipient.last_name || ''}`;
  }
  return transfer.recipient_id ? `User #${transfer.recipient_id}` : 'N/A';
}

/**
 * Update top items chart with data
 */
function updateTopItemsChart(data) {
  console.log('Dashboard: Updating top items chart');
  
  if (!window.topItemsChart) {
    console.warn('Dashboard: topItemsChart not initialized');
    return;
  }
  
  if (!data || !Array.isArray(data) || data.length === 0) {
    console.warn('Dashboard: No item data available for chart');
    window.topItemsChart.data.labels = ['No data available'];
    window.topItemsChart.data.datasets[0].data = [0];
    window.topItemsChart.options.plugins.title.text = 'No Item Revenue Data Available';
    window.topItemsChart.update();
    return;
  }
  
  // Sort data by revenue and limit to top 5
  const sortedData = [...data]
    .sort((a, b) => {
      const revenueA = parseFloat(a.total_revenue) || 0;
      const revenueB = parseFloat(b.total_revenue) || 0;
      return revenueB - revenueA;
    })
    .slice(0, 5);
  
  // Handle item names - ensuring each one is a simple string value
  const labels = sortedData.map(item => {
    // Ensure it's a simple string
    if (typeof item.item === 'string') {
      return item.item;
    } else if (item.item && Array.isArray(item.item)) {
      return item.item[0] || 'Unknown'; // Take just the first value if it's an array
    } else {
      return String(item.item || 'Unknown');
    }
  });
  
  // Get revenue values
  const revenues = sortedData.map(item => parseFloat(item.total_revenue) || 0);
  
  // Update chart
  window.topItemsChart.data.labels = labels;
  window.topItemsChart.data.datasets[0].data = revenues;
  window.topItemsChart.options.plugins.title.text = 'Top Items by Revenue';
  window.topItemsChart.update();
  
  console.log('Dashboard: Items chart updated with data');
}

/**
 * Update top stores chart with data
 */
function updateTopStoresChart(data) {
  console.log('Dashboard: Updating top stores chart');
  
  if (!window.topStoresChart) {
    console.warn('Dashboard: topStoresChart not initialized');
    return;
  }
  
  if (!data || !Array.isArray(data) || data.length === 0) {
    console.warn('Dashboard: No store data available for chart');
    window.topStoresChart.data.labels = ['No data available'];
    window.topStoresChart.data.datasets[0].data = [0];
    window.topStoresChart.options.plugins.title.text = 'No Store Revenue Data Available';
    window.topStoresChart.update();
    return;
  }
  
  // Sort data by revenue and limit to top 5
  const sortedData = [...data]
    .sort((a, b) => {
      const revenueA = parseFloat(a.total_revenue) || 0;
      const revenueB = parseFloat(b.total_revenue) || 0;
      return revenueB - revenueA;
    })
    .slice(0, 5);
  
  // Handle store names - ensuring each one is a simple string value
  const labels = sortedData.map(store => {
    // Ensure it's a simple string
    if (typeof store.store === 'string') {
      return store.store;
    } else if (store.store && Array.isArray(store.store)) {
      return store.store[0] || 'Unknown'; // Take just the first value if it's an array
    } else {
      return String(store.store || 'Unknown');
    }
  });
  
  // Get revenue values
  const revenues = sortedData.map(store => parseFloat(store.total_revenue) || 0);
  
  // Update chart
  window.topStoresChart.data.labels = labels;
  window.topStoresChart.data.datasets[0].data = revenues;
  window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
  window.topStoresChart.update();
  
  console.log('Dashboard: Stores chart updated with data');
}