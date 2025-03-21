/**
 * Analytics JavaScript for Venmito
 * 
 * This file handles the analytics page functionality, including:
 * - Loading and displaying analytics data
 * - Rendering various charts and visualizations
 * - Handling time period selections
 * - Displaying tables with top users
 */

// Store current state
const state = {
    timePeriod: 30, // Default to 30 days
    charts: {}
  };
  
  document.addEventListener('DOMContentLoaded', async () => {
    // Initialize charts with loading state
    initializeCharts();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial analytics data
    await loadAnalyticsData();
  });
  
  /**
   * Initialize charts with loading state
   */
  function initializeCharts() {
    // Create spending distribution chart
    const spendingDistCtx = document.getElementById('spending-distribution-chart');
    if (spendingDistCtx) {
      state.charts.spendingDistribution = new Chart(spendingDistCtx, {
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
    
    
    // Create transfer distribution chart
    const transferDistCtx = document.getElementById('transfer-distribution-chart');
    if (transferDistCtx) {
      state.charts.transferDistribution = new Chart(transferDistCtx, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [{
            label: 'Number of Transfers',
            data: [],
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading transfer distribution...'
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
    
    // Create popular items trend chart
    const popularItemsCtx = document.getElementById('popular-items-trend-chart');
    if (popularItemsCtx) {
      state.charts.popularItems = new Chart(popularItemsCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: []
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading popular items trend...'
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
    
    // Create time period transactions chart
    const timeTransactionsCtx = document.getElementById('time-transactions-chart');
    if (timeTransactionsCtx) {
      state.charts.timeTransactions = new Chart(timeTransactionsCtx, {
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
              text: 'Loading transactions data...'
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
    
    // Create time period transfers chart
    const timeTransfersCtx = document.getElementById('time-transfers-chart');
    if (timeTransfersCtx) {
      state.charts.timeTransfers = new Chart(timeTransfersCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: 'Transfer Volume',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Loading transfers data...'
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
  }
  
  /**
   * Set up event listeners for the page
   */
  function setupEventListeners() {
    // Time period select change
    document.getElementById('time-period')?.addEventListener('change', (e) => {
      state.timePeriod = parseInt(e.target.value);
    });
    
    // Update time charts button click
    document.getElementById('update-time-charts')?.addEventListener('click', () => {
      loadTimePeriodData();
    });
  }
  
  /**
   * Load all analytics data
   */
  async function loadAnalyticsData() {
    try {
      // Load spending distribution data
      const spendingDistribution = await API.analytics.getUserSpendingDistribution();
      updateSpendingDistributionChart(spendingDistribution);
      
      // Load transfer distribution data
      const transferDistribution = await API.analytics.getTransferAmountDistribution();
      updateTransferDistributionChart(transferDistribution);
      
      // Load popular items trend data
      const popularItems = await API.analytics.getPopularItemsByMonth(12);
      updatePopularItemsChart(popularItems);
      
      // Load time period data (initially 30 days)
      await loadTimePeriodData();
      
      // Load top users data
      await loadTopUsersData();
      
      // Update summary statistics cards
      updateStatisticsCards();
      
    } catch (error) {
      console.error('Error loading analytics data:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Load time period data based on selected time period
   */
  async function loadTimePeriodData() {
    try {
      // Load daily transactions data
      const transactions = await API.analytics.getDailyTransactionsSummary(state.timePeriod);
      updateTimeTransactionsChart(transactions);
      
      // Load daily transfers data
      const transfers = await API.analytics.getDailyTransfersSummary(state.timePeriod);
      updateTimeTransfersChart(transfers);
    } catch (error) {
      console.error('Error loading time period data:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Load top users data
   */
  async function loadTopUsersData() {
    try {
      // Load top users by spending
      const topSpenders = await API.analytics.getTopUsersBySpending(5);
      updateTopSpendersTable(topSpenders);
      
      // Load top users by transfers
      const topTransferers = await API.analytics.getTopUsersByTransfers(5);
      updateTopTransferersTable(topTransferers);
    } catch (error) {
      console.error('Error loading top users data:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Update spending distribution chart with data
   * 
   * @param {Array} data - Spending distribution data
   */
  function updateSpendingDistributionChart(data) {
    if (!state.charts.spendingDistribution || !data || data.length === 0) return;
    
    // Format data for chart
    const labels = data.map(item => `${item.range} (${item.percentage}%)`);
    const values = data.map(item => item.count);
    
    // Update chart data
    state.charts.spendingDistribution.data.labels = labels;
    state.charts.spendingDistribution.data.datasets[0].data = values;
    state.charts.spendingDistribution.options.plugins.title.text = 'User Spending Distribution';
    state.charts.spendingDistribution.update();
  }
  
  /**
   * Update transfer distribution chart with data
   * 
   * @param {Array} data - Transfer distribution data
   */
  function updateTransferDistributionChart(data) {
    if (!state.charts.transferDistribution || !data || data.length === 0) return;
    
    // Format data for chart
    const labels = data.map(item => item.range);
    const values = data.map(item => item.count);
    
    // Update chart data
    state.charts.transferDistribution.data.labels = labels;
    state.charts.transferDistribution.data.datasets[0].data = values;
    state.charts.transferDistribution.options.plugins.title.text = 'Transfer Amount Distribution';
    state.charts.transferDistribution.update();
  }
  
  /**
   * Update popular items chart with data
   * 
   * @param {Array} data - Popular items data
   */
  function updatePopularItemsChart(data) {
    if (!state.charts.popularItems || !data || data.length === 0) return;
    
    // Process the data to get unique months and items
    const months = [...new Set(data.map(item => item.month))].sort();
    const itemNames = [...new Set(data.map(item => item.item))];
    
    // Create datasets for each item
    const datasets = itemNames.map((item, index) => {
      const itemData = data.filter(d => d.item === item);
      const monthlyData = months.map(month => {
        const monthItem = itemData.find(d => d.month === month);
        return monthItem ? monthItem.sales : 0;
      });
      
      return {
        label: item,
        data: monthlyData,
        borderColor: API.generateChartColors(itemNames.length)[index],
        backgroundColor: API.generateChartColors(itemNames.length)[index].replace('0.7', '0.1'),
        borderWidth: 2,
        tension: 0.3
      };
    });
    
    // Update chart data
    state.charts.popularItems.data.labels = months;
    state.charts.popularItems.data.datasets = datasets;
    state.charts.popularItems.options.plugins.title.text = 'Monthly Popular Items Trend';
    state.charts.popularItems.update();
  }
  
  /**
   * Update time transactions chart with data
   * 
   * @param {Array} data - Daily transactions data
   */
  function updateTimeTransactionsChart(data) {
    if (!state.charts.timeTransactions || !data || data.length === 0) return;
    
    // Format data for chart
    const labels = data.map(item => API.formatDate(item.date));
    const values = data.map(item => item.amount);
    
    // Update chart data
    state.charts.timeTransactions.data.labels = labels;
    state.charts.timeTransactions.data.datasets[0].data = values;
    state.charts.timeTransactions.options.plugins.title.text = `Daily Transaction Volume (Last ${state.timePeriod} Days)`;
    state.charts.timeTransactions.update();
  }
  
  /**
   * Update time transfers chart with data
   * 
   * @param {Array} data - Daily transfers data
   */
  function updateTimeTransfersChart(data) {
    if (!state.charts.timeTransfers || !data || data.length === 0) return;
    
    // Format data for chart
    const labels = data.map(item => API.formatDate(item.date));
    const values = data.map(item => item.amount);
    
    // Update chart data
    state.charts.timeTransfers.data.labels = labels;
    state.charts.timeTransfers.data.datasets[0].data = values;
    state.charts.timeTransfers.options.plugins.title.text = `Daily Transfer Volume (Last ${state.timePeriod} Days)`;
    state.charts.timeTransfers.update();
  }
  
  /**
   * Update top spenders table with data
   * 
   * @param {Array} data - Top spenders data
   */
  function updateTopSpendersTable(data) {
    const tableBody = document.getElementById('top-spenders-table')?.querySelector('tbody');
    
    if (!tableBody) return;
    
    if (!data || data.length === 0) {
      // If no data, use the existing mock data in the HTML
      return;
    }
    
    tableBody.innerHTML = data.map(user => `
      <tr>
        <td>${user.first_name} ${user.last_name}</td>
        <td>${user.email}</td>
        <td>${API.formatCurrency(user.total_spent)}</td>
        <td>${API.formatCurrency(user.average_transaction)}</td>
        <td>${user.transaction_count}</td>
      </tr>
    `).join('');
  }
  
  /**
   * Update top transferers table with data
   * 
   * @param {Array} data - Top transferers data
   */
  function updateTopTransferersTable(data) {
    const tableBody = document.getElementById('top-transferers-table')?.querySelector('tbody');
    
    if (!tableBody) return;
    
    if (!data || data.length === 0) {
      // If no data, use the existing mock data in the HTML
      return;
    }
    
    tableBody.innerHTML = data.map(user => `
      <tr>
        <td>${user.first_name} ${user.last_name}</td>
        <td>${user.email}</td>
        <td>${API.formatCurrency(user.total_volume)}</td>
        <td>${API.formatCurrency(user.total_sent)}</td>
        <td>${API.formatCurrency(user.total_received)}</td>
        <td>${user.transfer_count}</td>
      </tr>
    `).join('');
  }
  
  /**
   * Update statistics summary cards
   */
  function updateStatisticsCards() {
    // Since we don't have direct API endpoints for these stats, 
    // we're using the pre-filled data in the HTML for now.
    // In a real implementation, you would fetch this data from the API.
  }