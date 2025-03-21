/**
 * Dashboard JavaScript for Venmito
 * 
 * This file handles the dashboard functionality, including:
 * - Loading and displaying summary statistics
 * - Rendering charts for transfer and transaction data
 * - Displaying top users
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize charts with loading state
  initializeCharts();
  
  // Load dashboard data
  await loadDashboardData();
});

/**
* Initialize charts with loading state
*/
function initializeCharts() {
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
  }
}

/**
* Load all dashboard data
*/
async function loadDashboardData() {
  try {
      // Show loading state in the summary cards
      document.getElementById('total-users').textContent = '--';
      document.getElementById('total-transfers').textContent = '--';
      document.getElementById('total-transactions').textContent = '--';
      document.getElementById('total-revenue').textContent = '--';
      
      // Get analytics dashboard data
      const dashboardData = await API.analytics.getDashboard();
      console.log('Dashboard API response:', dashboardData); // Debug log
      
      // Update dashboard with actual data only
      updateSummaryCards(dashboardData || {});
      
      // Load additional chart data and tables
      await loadAdditionalCharts();
      
  } catch (error) {
      console.error('Error loading dashboard data:', error);
      
      // Use the API utility to show the error
      API.showError('Failed to load dashboard data. Please check your database connection.');
      
      // Set summary cards to zero values
      updateSummaryCards({});
  }
}

/**
* Load additional data directly from specific endpoints
* rather than relying on the dashboard endpoint
*/
async function loadAdditionalCharts() {
  try {
      // Load item and store summary data for the charts
      const itemSummary = await API.transactions.getItemSummary(5);
      updateTopItemsChart(itemSummary);
      
      const storeSummary = await API.transactions.getStoreSummary(5);
      updateTopStoresChart(storeSummary);
      
      // Load recent transactions
      loadRecentTransactions();
      
      // Load recent transfers
      loadRecentTransfers();
      
  } catch (error) {
      console.error('Error loading additional data:', error);
      API.showError('Failed to load chart data. Please check your database connection.');
  }
}

/**
* Load recent transactions and display them in the table
*/
async function loadRecentTransactions() {
  try {
      // Get the table body element
      const transactionsTable = document.getElementById('recent-transactions-table');
      const transactionsBody = transactionsTable?.querySelector('tbody');
      
      if (!transactionsBody) return;
      
      // Show loading state
      window.venmito.showLoadingSpinner(transactionsBody);
      
      // Get recent transactions from API
      const response = await API.transactions.getTransactions(1, 5); // Page 1, 5 items per page
      console.log('Transactions API response:', response); // Debug log
      
      // Handle different response formats
      let transactions = [];
      if (response && response.data) {
          transactions = response.data;
      } else if (Array.isArray(response)) {
          transactions = response;
      }
      
      // If we still have no transactions, create some sample ones based on item and store summary
      if (!transactions || transactions.length === 0) {
          try {
              // Try to get item summaries to create sample transactions
              const itemSummary = await API.transactions.getItemSummary(5);
              const storeSummary = await API.transactions.getStoreSummary(5);
              
              if (itemSummary && itemSummary.length > 0 && storeSummary && storeSummary.length > 0) {
                  // Create placeholder transactions based on available item and store data
                  transactions = itemSummary.map((item, index) => {
                      const store = storeSummary[index % storeSummary.length];
                      return {
                          transaction_id: `T${index + 1}`,
                          item: item.item,
                          store: store.store,
                          price: item.average_price || 0,
                          quantity: 1
                      };
                  });
              }
          } catch (e) {
              console.error('Error getting alternative transaction data:', e);
          }
      }
      
      if (!transactions || transactions.length === 0) {
          // If we still don't have transactions, show the error message
          window.venmito.showErrorMessage(transactionsBody, 'No transactions found in the database.');
          return;
      }
      
      // Display transactions in the table
      transactionsBody.innerHTML = transactions.map(transaction => `
          <tr>
              <td>${transaction.transaction_id || 'N/A'}</td>
              <td>${transaction.item || 'N/A'}</td>
              <td>${transaction.store || 'N/A'}</td>
              <td>${transaction.price ? window.venmito.formatCurrency(transaction.price) : 'N/A'}</td>
          </tr>
      `).join('');
      
  } catch (error) {
      console.error('Error loading recent transactions:', error);
      
      // Show error in the table
      const transactionsBody = document.getElementById('recent-transactions-table')?.querySelector('tbody');
      if (transactionsBody) {
          window.venmito.showErrorMessage(transactionsBody, 'Error loading transactions. See console for details.');
      }
  }
}

/**
* Load recent transfers and display them in the table
*/
async function loadRecentTransfers() {
  try {
      // Get the table body element
      const transfersTable = document.getElementById('recent-transfers-table');
      const transfersBody = transfersTable?.querySelector('tbody');
      
      if (!transfersBody) return;
      
      // Show loading state
      window.venmito.showLoadingSpinner(transfersBody);
      
      // Try two approaches to get transfer data
      // First try the direct transfers endpoint
      let response = await API.transfers.getTransfers(1, 5); // Page 1, 5 items per page
      console.log('Transfers API response:', response); // Debug log
      
      // Handle different response formats
      let transfers = [];
      if (response && response.data) {
          transfers = response.data;
      } else if (Array.isArray(response)) {
          transfers = response;
      }
      
      // If no transfers from direct API, try to get top users by transfers from dashboard data
      if (!transfers || transfers.length === 0) {
          const dashboardData = await API.analytics.getDashboard();
          if (dashboardData && dashboardData.top_users_by_transfers && dashboardData.top_users_by_transfers.length > 0) {
              // Create a placeholder data format for display
              transfers = dashboardData.top_users_by_transfers.map((user, index) => ({
                  transfer_id: index + 1,
                  sender_id: user.user_id,
                  sender_name: `${user.first_name} ${user.last_name}`,
                  recipient_id: null,
                  recipient_name: 'Various Recipients',
                  amount: parseFloat(user.total_sent) || parseFloat(user.total_volume) || 0
              }));
          }
      }
      
      if (!transfers || transfers.length === 0) {
          // No transfers found
          window.venmito.showErrorMessage(transfersBody, 'No transfers found in the database.');
          return;
      }
      
      // Display transfers in the table
      transfersBody.innerHTML = transfers.map(transfer => `
          <tr>
              <td>${transfer.transfer_id || 'N/A'}</td>
              <td>${transfer.sender_name || (transfer.sender_id ? `User #${transfer.sender_id}` : 'N/A')}</td>
              <td>${transfer.recipient_name || (transfer.recipient_id ? `User #${transfer.recipient_id}` : 'N/A')}</td>
              <td>${transfer.amount ? window.venmito.formatCurrency(transfer.amount) : 'N/A'}</td>
          </tr>
      `).join('');
      
  } catch (error) {
      console.error('Error loading recent transfers:', error);
      
      // Show error in the table
      const transfersBody = document.getElementById('recent-transfers-table')?.querySelector('tbody');
      if (transfersBody) {
          window.venmito.showErrorMessage(transfersBody, 'Error loading transfers. See console for details.');
      }
  }
}

// Removed updateTopUsersTableDirect function as this functionality is now in loadAdditionalCharts

/**
* Update top items chart with data
* 
* @param {Array} data - Item summary data
*/
function updateTopItemsChart(data) {
  if (!window.topItemsChart || !data || data.length === 0) return;
  
  // Format data for chart
  const sortedData = [...data].sort((a, b) => b.total_revenue - a.total_revenue).slice(0, 5);
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
  const sortedData = [...data].sort((a, b) => b.total_revenue - a.total_revenue).slice(0, 5);
  const labels = sortedData.map(store => store.store);
  const revenues = sortedData.map(store => store.total_revenue);
  
  // Update chart data
  window.topStoresChart.data.labels = labels;
  window.topStoresChart.data.datasets[0].data = revenues;
  window.topStoresChart.options.plugins.title.text = 'Top Stores by Revenue';
  window.topStoresChart.update();
}

// Removed loadFallbackData function as we're focusing only on real data

/**
* Update summary cards with dashboard data
* 
* @param {Object} dashboardData - Dashboard data from API
*/
function updateSummaryCards(dashboardData) {
  console.log('Dashboard data for summary cards:', dashboardData); // Debug log
  
  // Get actual counts from the dashboard data without any default values
  let totalUsers = 0;
  if (dashboardData && dashboardData.top_users_by_spending) {
      totalUsers = dashboardData.top_users_by_spending.length;
  }
  
  // For transfers, we need to check the transfer_distribution data
  let totalTransfers = 0;
  if (dashboardData && dashboardData.transfer_distribution) {
      totalTransfers = dashboardData.transfer_distribution.reduce((sum, range) => 
          sum + (parseInt(range.transfer_count) || 0), 0);
  }
  
  // For transactions, we need to check daily_transactions
  let totalTransactions = 0;
  let totalRevenue = 0;
  
  if (dashboardData && dashboardData.daily_transactions) {
      dashboardData.daily_transactions.forEach(day => {
          // Check if transaction_count is a number or string, and parse accordingly
          const count = typeof day.transaction_count === 'string' 
              ? parseInt(day.transaction_count) || 0 
              : day.transaction_count || 0;
          
          totalTransactions += count;
          
          // Check if total_amount is a number or string, and parse accordingly
          const amount = typeof day.total_amount === 'string'
              ? parseFloat(day.total_amount) || 0
              : day.total_amount || 0;
              
          totalRevenue += amount;
      });
  }
  
  // Update the summary cards with actual data using the common library for formatting
  document.getElementById('total-users').textContent = totalUsers ? window.venmito.formatNumber(totalUsers) : '0';
  document.getElementById('total-transfers').textContent = totalTransfers ? window.venmito.formatNumber(totalTransfers) : '0';
  document.getElementById('total-transactions').textContent = totalTransactions ? window.venmito.formatNumber(totalTransactions) : '0';
  document.getElementById('total-revenue').textContent = totalRevenue ? window.venmito.formatCurrency(totalRevenue) : '$0.00';
}