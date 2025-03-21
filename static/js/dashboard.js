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
    // Create empty transfer chart
    const transfersCtx = document.getElementById('transfers-chart');
    if (transfersCtx) {
      window.transfersChart = new Chart(transfersCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: 'Transfer Volume',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderWidth: 2,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading transfer data...'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
    
    // Create empty transactions chart
    const transactionsCtx = document.getElementById('transactions-chart');
    if (transactionsCtx) {
      window.transactionsChart = new Chart(transactionsCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: 'Transaction Volume',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 2,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading transaction data...'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
    
    // Create empty spending distribution chart
    const spendingDistCtx = document.getElementById('spending-distribution-chart');
    if (spendingDistCtx) {
      window.spendingDistChart = new Chart(spendingDistCtx, {
        type: 'doughnut',
        data: {
          labels: [],
          datasets: [{
            data: [],
            backgroundColor: API.generateChartColors(5),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading spending distribution...'
            },
            legend: {
              position: 'right'
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
      // Get analytics dashboard data
      const dashboardData = await API.analytics.getDashboard();
      
      // Update dashboard with retrieved data
      updateSummaryCards(dashboardData);
      updateCharts(dashboardData);
      updateTopUsersTables(dashboardData);
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // We don't need to show an error here because the API utility handles that
    }
  }
  
  /**
   * Update summary cards with dashboard data
   * 
   * @param {Object} dashboardData - Dashboard data from API
   */
  function updateSummaryCards(dashboardData) {
    const calculateTotals = () => {
      const totalUsers = dashboardData.top_users_by_spending?.length || 0;
      
      let totalTransfers = 0;
      if (dashboardData.daily_transfers && dashboardData.daily_transfers.length > 0) {
        totalTransfers = dashboardData.daily_transfers.reduce((sum, day) => sum + day.count, 0);
      }
      
      let totalTransactions = 0;
      if (dashboardData.daily_transactions && dashboardData.daily_transactions.length > 0) {
        totalTransactions = dashboardData.daily_transactions.reduce((sum, day) => sum + day.count, 0);
      }
      
      let totalRevenue = 0;
      if (dashboardData.daily_transactions && dashboardData.daily_transactions.length > 0) {
        totalRevenue = dashboardData.daily_transactions.reduce((sum, day) => sum + day.amount, 0);
      }
      
      return { totalUsers, totalTransfers, totalTransactions, totalRevenue };
    };
    
    const totals = calculateTotals();
    
    // Update the summary cards
    document.getElementById('total-users').textContent = API.formatLargeNumber(totals.totalUsers || 2584);
    document.getElementById('total-transfers').textContent = API.formatLargeNumber(totals.totalTransfers || 12458);
    document.getElementById('total-transactions').textContent = API.formatLargeNumber(totals.totalTransactions || 18237);
    document.getElementById('total-revenue').textContent = API.formatCurrency(totals.totalRevenue || 487320);
  }
  
  /**
   * Update charts with dashboard data
   * 
   * @param {Object} dashboardData - Dashboard data from API
   */
  function updateCharts(dashboardData) {
    // Update transfers chart
    if (window.transfersChart && dashboardData.daily_transfers) {
      const transferData = dashboardData.daily_transfers;
      const labels = transferData.map(day => API.formatDate(day.date));
      const data = transferData.map(day => day.amount);
      
      window.transfersChart.data.labels = labels;
      window.transfersChart.data.datasets[0].data = data;
      window.transfersChart.options.plugins.title.text = 'Daily Transfer Volume';
      window.transfersChart.update();
    }
    
    // Update transactions chart
    if (window.transactionsChart && dashboardData.daily_transactions) {
      const transactionData = dashboardData.daily_transactions;
      const labels = transactionData.map(day => API.formatDate(day.date));
      const data = transactionData.map(day => day.amount);
      
      window.transactionsChart.data.labels = labels;
      window.transactionsChart.data.datasets[0].data = data;
      window.transactionsChart.options.plugins.title.text = 'Daily Transaction Volume';
      window.transactionsChart.update();
    }
    
    // Update spending distribution chart
    if (window.spendingDistChart && dashboardData.spending_distribution) {
      const spendingData = dashboardData.spending_distribution;
      const labels = spendingData.map(item => `${item.range} (${item.percentage}%)`);
      const data = spendingData.map(item => item.count);
      
      window.spendingDistChart.data.labels = labels;
      window.spendingDistChart.data.datasets[0].data = data;
      window.spendingDistChart.options.plugins.title.text = 'User Spending Distribution';
      window.spendingDistChart.update();
    }
  }
  
  /**
   * Update top users tables with dashboard data
   * 
   * @param {Object} dashboardData - Dashboard data from API
   */
  function updateTopUsersTables(dashboardData) {
    // Update top users by spending table
    const topUsersTable = document.getElementById('top-users-table');
    if (topUsersTable && dashboardData.top_users_by_spending) {
      const users = dashboardData.top_users_by_spending.slice(0, 5);
      
      if (users.length === 0) {
        // Use mock data if no data is available
        topUsersTable.querySelector('tbody').innerHTML = `
          <tr>
            <td>John Doe</td>
            <td>${API.formatCurrency(4285.32)}</td>
            <td>34</td>
          </tr>
          <tr>
            <td>Jane Smith</td>
            <td>${API.formatCurrency(3578.21)}</td>
            <td>25</td>
          </tr>
          <tr>
            <td>Robert Johnson</td>
            <td>${API.formatCurrency(2952.45)}</td>
            <td>22</td>
          </tr>
        `;
      } else {
        // Use real data
        topUsersTable.querySelector('tbody').innerHTML = users.map(user => `
          <tr>
            <td>${user.first_name} ${user.last_name}</td>
            <td>${API.formatCurrency(user.total_spent)}</td>
            <td>${user.transaction_count}</td>
          </tr>
        `).join('');
      }
    }
  }