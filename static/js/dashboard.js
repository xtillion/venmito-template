/**
 * Dashboard JavaScript for Venmito
 *
 * This simplified script loads and displays dashboard data including:
 * - Summary statistics (users, transfers, transactions, revenue)
 * - Top items and stores by revenue
 * - Top transactions by amount
 * - Recent transfers
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Dashboard: Initializing...');
  
  // Update section titles
  updateSectionTitles();
  
  // Initialize charts with loading state
  initializeCharts();
  
  // Set default values while data loads
  setDefaultSummaryValues();
  
  // Load all dashboard data
  try {
    await loadDashboardData();
    console.log('Dashboard: Data loaded successfully');
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
    window.API.showError('Failed to load dashboard data. Please refresh the page.');
  }
});

/**
 * Update section titles to match requirements
 */
function updateSectionTitles() {
  // Update transactions table title
  const transactionsHeader = document.querySelector('#recent-transactions-table')?.closest('.card')?.querySelector('.card-header');
  if (transactionsHeader) {
    transactionsHeader.textContent = 'Top Transactions by Amount';
  }
  
  // Update transfers table title (if needed)
  const transfersHeader = document.querySelector('#recent-transfers-table')?.closest('.card')?.querySelector('.card-header');
  if (transfersHeader && !transfersHeader.textContent.includes('Recent')) {
    transfersHeader.textContent = 'Recent Transfers';
  }
}

/**
 * Initialize charts with loading state
 */
function initializeCharts() {
  console.log('Dashboard: Initializing charts');
  
  // Initialize top items chart
  initializeTopItemsChart();
  
  // Initialize top stores chart
  initializeTopStoresChart();
}

/**
 * Initialize top items chart
 */
function initializeTopItemsChart() {
  const canvas = document.getElementById('top-items-chart');
  if (!canvas) {
    console.warn('Top items chart element not found');
    return;
  }
  
  try {
    window.topItemsChart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: ['Loading...'],
        datasets: [{
          label: 'Revenue',
          data: [0],
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Top Items by Revenue - Loading...'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Revenue ($)'
            }
          }
        }
      }
    });
    console.log('Top items chart initialized');
  } catch (err) {
    console.error('Failed to initialize top items chart:', err);
  }
}

/**
 * Initialize top stores chart
 */
function initializeTopStoresChart() {
  const canvas = document.getElementById('top-stores-chart');
  if (!canvas) {
    console.warn('Top stores chart element not found');
    return;
  }
  
  try {
    window.topStoresChart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: ['Loading...'],
        datasets: [{
          label: 'Revenue',
          data: [0],
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Top Stores by Revenue - Loading...'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Revenue ($)'
            }
          }
        }
      }
    });
    console.log('Top stores chart initialized');
  } catch (err) {
    console.error('Failed to initialize top stores chart:', err);
  }
}

/**
 * Set default values for summary cards
 */
function setDefaultSummaryValues() {
  const elements = {
    'total-users': '--',
    'total-transfers': '--',
    'total-transactions': '--',
    'total-revenue': '--'
  };
  
  for (const [id, value] of Object.entries(elements)) {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  }
}

/**
 * Update the top items chart
 * @param {Array} items Top items data
 */


/**
 * Update the top stores chart
 * @param {Array} stores Top stores data
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
  
  // Get item names (handling different possible API response formats)
  const labels = sortedData.map(item => {
    if (typeof item.item === 'string') {
      return item.item;
    } else if (item.item && Array.isArray(item.item)) {
      return item.item[0] || 'Unknown';
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
 * Update the transactions table in the dashboard
 * 
 * @param {Array} transactions The transactions data
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
  
  // Display transactions with item display based on new schema
  transactionsBody.innerHTML = topTransactions.map(transaction => {
    // Format item display based on available data
    let itemDisplay = 'N/A';
    
    // Check different possible item-related fields based on API response
    if (transaction.first_item) {
      // If the API returns the first item directly
      itemDisplay = transaction.first_item;
    } else if (transaction.item_count > 1) {
      // If the API returns an item count
      itemDisplay = `${transaction.item_count} items`;
    } else if (transaction.items && transaction.items.length > 0) {
      // If we have the items array (from a detailed fetch)
      itemDisplay = transaction.items.length > 1 
        ? `${transaction.items.length} items` 
        : transaction.items[0].item;
    } else if (transaction.item) {
      // For backward compatibility with old schema
      itemDisplay = transaction.item;
    }
    
    return `
      <tr>
        <td>${transaction.transaction_id || 'N/A'}</td>
        <td>${itemDisplay}</td>
        <td>${transaction.store || 'N/A'}</td>
        <td>${transaction.price ? formatCurrency(transaction.price) : 'N/A'}</td>
      </tr>
    `;
  }).join('');
  
  console.log('Dashboard: Transactions table updated');
}

/**
 * Update transfers table
 * @param {Array} transfers Transfer data
 */
function updateTransfersTable(transfers) {
  const tableBody = document.querySelector('#recent-transfers-table tbody');
  if (!tableBody || !Array.isArray(transfers)) {
    console.warn('Cannot update transfers table: Table not found or invalid data');
    return;
  }
  
  if (transfers.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No transfers available</td></tr>';
    return;
  }
  
  // Create table rows
  const rows = transfers.map(transfer => `
    <tr>
      <td>${transfer.transfer_id || 'N/A'}</td>
      <td>${getSenderName(transfer)}</td>
      <td>${getRecipientName(transfer)}</td>
      <td>${window.API.formatCurrency(transfer.amount || 0)}</td>
    </tr>
  `).join('');
  
  tableBody.innerHTML = rows;
  console.log('Transfers table updated');
}

/**
 * Get sender name from transfer object
 * @param {Object} transfer Transfer object
 * @returns {string} Formatted sender name
 */
function getSenderName(transfer) {
  if (transfer.sender_name) {
    return transfer.sender_name;
  }
  if (transfer.sender && transfer.sender.first_name) {
    return `${transfer.sender.first_name} ${transfer.sender.last_name || ''}`.trim();
  }
  return transfer.sender_id ? `User #${transfer.sender_id}` : 'N/A';
}

/**
 * Get recipient name from transfer object
 * @param {Object} transfer Transfer object
 * @returns {string} Formatted recipient name
 */
function getRecipientName(transfer) {
  if (transfer.recipient_name) {
    return transfer.recipient_name;
  }
  if (transfer.recipient && transfer.recipient.first_name) {
    return `${transfer.recipient.first_name} ${transfer.recipient.last_name || ''}`.trim();
  }
  return transfer.recipient_id ? `User #${transfer.recipient_id}` : 'N/A';
}

/**
 * Display error message in a table
 * 
 * @param {string} tableId ID of the table element
 * @param {string} message Error message to display
 */
function showTableError(tableId, message = 'Failed to load data') {
  const tableBody = document.getElementById(tableId)?.querySelector('tbody');
  if (tableBody) {
    tableBody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">${message}</td></tr>`;
  }
}

/**
 * Update the summary cards with dashboard totals
 * 
 * @param {Object} totals Dashboard totals data
 */
function updateSummaryCards(totals) {
  // Update total revenue
  const revenueElement = document.getElementById('total-revenue');
  if (revenueElement) {
    revenueElement.textContent = window.API.formatCurrency(totals.total_revenue || 0);
  }
  
  // Update total transactions
  const transactionsElement = document.getElementById('total-transactions');
  if (transactionsElement) {
    transactionsElement.textContent = window.API.formatLargeNumber(totals.total_transactions || 0);
  }
  
  // Update average transaction value if available
  const avgTransactionElement = document.getElementById('average-transaction-value');
  if (avgTransactionElement && totals.average_transaction_value) {
    avgTransactionElement.textContent = window.API.formatCurrency(totals.average_transaction_value);
  }
  
  // Update top selling item if available
  const topSellingItemElement = document.getElementById('top-selling-item');
  if (topSellingItemElement && totals.top_selling_item) {
    topSellingItemElement.textContent = totals.top_selling_item;
  }

  const transfersElement = document.getElementById('total-transfers');
  if (transfersElement) {
    transfersElement.textContent = window.API.formatLargeNumber(totals.total_transfers || 0);
  }

  const usersElement = document.getElementById('total-users');
  if (usersElement) {
    usersElement.textContent = window.API.formatLargeNumber(totals.total_users || 0);
  }
}

/**
 * Update top stores chart with data
 * 
 * @param {Array} data - Store summary data
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
  
  // Get store names
  const labels = sortedData.map(store => store.store);
  
  // Get revenue values
  const revenues = sortedData.map(store => parseFloat(store.total_revenue) || 0);
  
  // Update chart
  window.topStoresChart.data.labels = labels;
  window.topStoresChart.data.datasets[0].data = revenues;
  window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
  window.topStoresChart.update();
  
  console.log('Dashboard: Stores chart updated with data');
}

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
  try {
    console.log('Dashboard: Loading data...');
    
    // Fetch all required data in parallel
    const [
      dashboardTotals,
      topItems,
      topStores,
      topTransactions,
      transfers,
      users
    ] = await Promise.allSettled([
      window.API.analytics.getDashboardTotals(),
      window.API.analytics.getTopItems(5),
      window.API.transactions.getStoreSummary(5),
      window.API.fetch('/analytics/top-transactions?limit=5', {}, () => []),
      window.API.transfers.getTransfers(1, 5),
      window.API.people.getUsers(1, 1000) // Get user count
    ]);
    
    // Update summary cards with data from dashboardTotals
    if (dashboardTotals.status === 'fulfilled' && dashboardTotals.value) {
      updateSummaryCards(dashboardTotals.value);
    }
    
    // Update top items chart
    if (topItems.status === 'fulfilled' && topItems.value) {
      updateTopItemsChart(topItems.value);
    }
    
    // Update top stores chart
    if (topStores.status === 'fulfilled' && topStores.value) {
      updateTopStoresChart(topStores.value);
    }
    
    // Update transactions table with top transactions by amount
    if (topTransactions.status === 'fulfilled' && topTransactions.value) {
      updateTransactionsTable(topTransactions.value);
    } else {
      // Fallback to loading transactions directly if analytics endpoint fails
      try {
        const result = await window.API.transactions.getTransactions(1, 100);
        if (result && result.data && Array.isArray(result.data)) {
          // Sort by price and get top 5
          const sortedTransactions = result.data
            .filter(tx => tx && (tx.price !== undefined && tx.price !== null))
            .sort((a, b) => {
              const priceA = typeof a.price === 'string' ? parseFloat(a.price) : a.price;
              const priceB = typeof b.price === 'string' ? parseFloat(b.price) : b.price;
              return priceB - priceA;
            })
            .slice(0, 5);
            
          updateTransactionsTable(sortedTransactions);
        }
      } catch (error) {
        console.error('Alternative transactions approach failed:', error);
        showTableError('recent-transactions-table');
      }
    }
    
    // Update transfers table
    if (transfers.status === 'fulfilled' && transfers.value) {
      let transferData = [];
      
      if (transfers.value.data && Array.isArray(transfers.value.data)) {
        transferData = transfers.value.data;
      } else if (Array.isArray(transfers.value)) {
        transferData = transfers.value;
      }
      
      updateTransfersTable(transferData);
    } else {
      showTableError('recent-transfers-table');
    }
    
  } catch (error) {
    console.error('Error loading dashboard data:', error);
    throw error;
  }
}