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
function updateTopItemsChart(items) {
  if (!window.topItemsChart || !Array.isArray(items)) {
    console.warn('Cannot update top items chart: Chart not initialized or invalid data');
    return;
  }
  
  if (items.length === 0) {
    window.topItemsChart.data.labels = ['No data available'];
    window.topItemsChart.data.datasets[0].data = [0];
    window.topItemsChart.update();
    return;
  }
  
  // Sort items by revenue (highest first) and take top 5
  const topItems = items.sort((a, b) => (b.total_revenue || 0) - (a.total_revenue || 0)).slice(0, 5);
  
  // Prepare data for chart
  const labels = topItems.map(item => item.item || 'Unknown');
  const values = topItems.map(item => item.total_revenue || 0);
  
  // Generate colors
  const backgroundColors = window.API.generateChartColors(labels.length);
  const borderColors = backgroundColors.map(color => color.replace('0.7', '1'));
  
  // Update chart
  window.topItemsChart.data.labels = labels;
  window.topItemsChart.data.datasets[0].data = values;
  window.topItemsChart.data.datasets[0].backgroundColor = backgroundColors;
  window.topItemsChart.data.datasets[0].borderColor = borderColors;
  window.topItemsChart.options.plugins.title.text = 'Top Items by Revenue';
  window.topItemsChart.update();
  console.log('Top items chart updated');
}

/**
 * Update the top stores chart
 * @param {Array} stores Top stores data
 */
function updateTopStoresChart(stores) {
  if (!window.topStoresChart || !Array.isArray(stores)) {
    console.warn('Cannot update top stores chart: Chart not initialized or invalid data');
    return;
  }
  
  if (stores.length === 0) {
    window.topStoresChart.data.labels = ['No data available'];
    window.topStoresChart.data.datasets[0].data = [0];
    window.topStoresChart.update();
    return;
  }
  
  // Sort stores by revenue (highest first) and take top 5
  const topStores = stores.sort((a, b) => (b.total_revenue || 0) - (a.total_revenue || 0)).slice(0, 5);
  
  // Prepare data for chart
  const labels = topStores.map(store => store.store || 'Unknown');
  const values = topStores.map(store => store.total_revenue || 0);
  
  // Generate colors
  const backgroundColors = window.API.generateChartColors(labels.length);
  const borderColors = backgroundColors.map(color => color.replace('0.7', '1'));
  
  // Update chart
  window.topStoresChart.data.labels = labels;
  window.topStoresChart.data.datasets[0].data = values;
  window.topStoresChart.data.datasets[0].backgroundColor = backgroundColors;
  window.topStoresChart.data.datasets[0].borderColor = borderColors;
  window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
  window.topStoresChart.update();
  console.log('Top stores chart updated');
}

/**
 * Update transactions table with top transactions by amount
 * @param {Array} transactions Transaction data
 */
function updateTransactionsTable(transactions) {
  const tableBody = document.querySelector('#recent-transactions-table tbody');
  if (!tableBody || !Array.isArray(transactions)) {
    console.warn('Cannot update transactions table: Table not found or invalid data');
    return;
  }
  
  console.log(`Updating transactions table with ${transactions.length} transactions`);
  
  if (transactions.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No transactions available</td></tr>';
    return;
  }
  
  // Create table rows
  const rows = transactions.map(tx => {
    // Make sure we have valid data or provide defaults
    const txId = tx.transaction_id || 'N/A';
    const item = tx.item || 'Unknown Item';
    const store = tx.store || 'Unknown Store';
    const price = tx.price !== undefined && tx.price !== null ? tx.price : 0;
    
    return `
      <tr>
        <td>${txId}</td>
        <td>${item}</td>
        <td>${store}</td>
        <td>${window.API.formatCurrency(price)}</td>
      </tr>
    `;
  }).join('');
  
  tableBody.innerHTML = rows;
  console.log('Transactions table updated successfully');
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
      window.API.fetch('/api/analytics/top-transactions?limit=5', {}, () => []),
      window.API.transfers.getTransfers(1, 5),
      window.API.people.getUsers(1, 1000) // Get user count
    ]);
    
    // Update summary cards
    if (dashboardTotals.status === 'fulfilled' && dashboardTotals.value) {
      const totals = dashboardTotals.value;
      
      // Update summary cards with data
      const userElement = document.getElementById('total-users');
      if (userElement) {
        // Use the total from users API if available, fallback to dashboard totals
        let userCount = totals.total_users || 0;
        if (users.status === 'fulfilled' && users.value && users.value.pagination) {
          userCount = users.value.pagination.total || userCount;
        }
        userElement.textContent = window.API.formatLargeNumber(userCount);
      }
      
      const transfersElement = document.getElementById('total-transfers');
      if (transfersElement) {
        // Get total transfers count - either from totals or calculate
        let transferCount = totals.total_transfers || 0;
        if (transferCount === 0 && transfers.status === 'fulfilled' && transfers.value) {
          // If we have pagination info, use it
          if (transfers.value.pagination) {
            transferCount = transfers.value.pagination.total || 0;
          } else if (transfers.value.data && transfers.value.data.length > 0) {
            // Just show at least the count of what we have
            transferCount = transfers.value.data.length;
          }
        }
        transfersElement.textContent = window.API.formatLargeNumber(transferCount);
      }
      
      const transactionsElement = document.getElementById('total-transactions');
      if (transactionsElement) {
        // Get total transactions count - either from totals or calculate
        let transactionCount = totals.total_transactions || 0;
        if (transactionCount === 0 && transactions.status === 'fulfilled' && transactions.value) {
          // If we have pagination info, use it
          if (transactions.value.pagination) {
            transactionCount = transactions.value.pagination.total || 0;
          } else if (transactions.value.data && transactions.value.data.length > 0) {
            // Just show at least the count of what we have
            transactionCount = transactions.value.data.length;
          }
        }
        transactionsElement.textContent = window.API.formatLargeNumber(transactionCount);
      }
      
      const revenueElement = document.getElementById('total-revenue');
      if (revenueElement) {
        revenueElement.textContent = window.API.formatCurrency(totals.total_revenue || 0);
      }
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
      console.log('Processing top transactions for table');
      
      let transactionData = topTransactions.value;
      
      // Make sure we have an array
      if (!Array.isArray(transactionData)) {
        console.warn('Top transactions response is not an array:', transactionData);
        transactionData = [];
      }
      
      console.log(`Found ${transactionData.length} top transactions to display`);
      updateTransactionsTable(transactionData);
    } else {
      console.warn('Failed to load top transactions data:', 
                 topTransactions.status === 'rejected' ? topTransactions.reason : 'No data');
      
      // Try an alternative approach if the main one failed
      try {
        console.log('Trying alternative approach to get top transactions');
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
        
        // Show error message in the table
        const tableBody = document.querySelector('#recent-transactions-table tbody');
        if (tableBody) {
          tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Failed to load transaction data</td></tr>';
        }
      }
    }
    
    // Update transfers table with recent transfers
    if (transfers.status === 'fulfilled' && transfers.value) {
      console.log('Processing transfers for recent transfers table');
      
      let transferData = [];
      
      // Check if the data is in the expected format
      if (transfers.value.data && Array.isArray(transfers.value.data)) {
        transferData = transfers.value.data;
      } else if (Array.isArray(transfers.value)) {
        transferData = transfers.value;
      }
      
      console.log(`Found ${transferData.length} transfers to display`);
      updateTransfersTable(transferData);
    } else {
      console.warn('Failed to load transfers data:', 
                 transfers.status === 'rejected' ? transfers.reason : 'No data');
      
      // Show error message in the table
      const tableBody = document.querySelector('#recent-transfers-table tbody');
      if (tableBody) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Failed to load transfer data</td></tr>';
      }
    }
  } catch (error) {
    console.error('Error loading dashboard data:', error);
    throw error;
  }
}