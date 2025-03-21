// Set Chart.js global defaults for dark theme
Chart.defaults.color = '#b3b3b3';
Chart.defaults.borderColor = '#3d3d3d';
Chart.defaults.plugins.legend.labels.color = '#b3b3b3';
Chart.defaults.plugins.title.color = '#ffffff';

// Define chart color palette
const chartColors = {
  blue: '#4285f4',
  green: '#34a853',
  yellow: '#fbbc05',
  red: '#ea4335',
  purple: '#ab47bc',
  teal: '#26a69a',
  lightBlue: '#64b5f6',
  lightGreen: '#66bb6a',
  orange: '#ff9800',
  pink: '#ec407a'
};

document.addEventListener('DOMContentLoaded', function() {
  initializeCharts();
  fetchAnalyticsData();
});

// Initialize all charts
function initializeCharts() {
  // Spending Distribution Chart
  const spendingDistributionCtx = document.getElementById('spending-distribution-chart');
  if (spendingDistributionCtx) {
    window.spendingDistributionChart = new Chart(spendingDistributionCtx.getContext('2d'), {
      type: 'pie',
      data: {
        labels: ['Electronics', 'Clothing', 'Food & Dining', 'Entertainment', 'Travel', 'Other'],
        datasets: [{
          data: [35, 15, 20, 10, 12, 8],
          backgroundColor: [
            chartColors.blue,
            chartColors.green,
            chartColors.yellow,
            chartColors.red,
            chartColors.purple,
            chartColors.teal
          ],
          borderColor: '#1e1e1e',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
          },
          title: {
            display: true,
            text: 'Spending Categories (%)',
            padding: {
              top: 10,
              bottom: 20
            }
          }
        }
      }
    });
  }

  // Transfer Distribution Chart
  const transferDistributionCtx = document.getElementById('transfer-distribution-chart');
  if (transferDistributionCtx) {
    window.transferDistributionChart = new Chart(transferDistributionCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['$0-$20', '$21-$50', '$51-$100', '$101-$200', '$201-$500', '$500+'],
        datasets: [{
          label: 'Number of Transfers',
          data: [382, 724, 516, 298, 157, 84],
          backgroundColor: chartColors.purple,
          borderColor: chartColors.purple,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Transfers'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Amount Range'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Transfer Amount Distribution',
            padding: {
              top: 10,
              bottom: 20
            }
          }
        }
      }
    });
  }

  // Popular Items Trend Chart
  const popularItemsTrendCtx = document.getElementById('popular-items-trend-chart');
  if (popularItemsTrendCtx) {
    window.popularItemsTrendChart = new Chart(popularItemsTrendCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'Electronics',
            data: [42, 45, 38, 40, 48, 52, 54, 59, 63, 58, 65, 72],
            borderColor: chartColors.blue,
            backgroundColor: 'rgba(66, 133, 244, 0.2)',
            tension: 0.3,
            fill: true
          },
          {
            label: 'Clothing',
            data: [28, 30, 34, 32, 36, 39, 35, 38, 40, 42, 46, 51],
            borderColor: chartColors.green,
            backgroundColor: 'rgba(52, 168, 83, 0.2)',
            tension: 0.3,
            fill: true
          },
          {
            label: 'Food & Dining',
            data: [35, 36, 37, 38, 40, 42, 44, 46, 48, 49, 50, 52],
            borderColor: chartColors.yellow,
            backgroundColor: 'rgba(251, 188, 5, 0.2)',
            tension: 0.3,
            fill: true
          },
          {
            label: 'Entertainment',
            data: [22, 24, 26, 28, 30, 33, 35, 37, 38, 40, 42, 45],
            borderColor: chartColors.red,
            backgroundColor: 'rgba(234, 67, 53, 0.2)',
            tension: 0.3,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Purchases'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Month'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Popular Items by Month',
            padding: {
              top: 10,
              bottom: 20
            }
          }
        }
      }
    });
  }

  // Time Transactions Chart
  const timeTransactionsCtx = document.getElementById('time-transactions-chart');
  if (timeTransactionsCtx) {
    window.timeTransactionsChart = new Chart(timeTransactionsCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
        datasets: [{
          label: 'Transactions',
          data: Array.from({length: 30}, () => Math.floor(Math.random() * 50) + 30),
          borderColor: chartColors.teal,
          backgroundColor: 'rgba(38, 166, 154, 0.2)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Transactions'
            }
          }
        }
      }
    });
  }

  // Time Transfers Chart
  const timeTransfersCtx = document.getElementById('time-transfers-chart');
  if (timeTransfersCtx) {
    window.timeTransfersChart = new Chart(timeTransfersCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
        datasets: [{
          label: 'Transfers',
          data: Array.from({length: 30}, () => Math.floor(Math.random() * 40) + 20),
          borderColor: chartColors.lightBlue,
          backgroundColor: 'rgba(100, 181, 246, 0.2)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Transfers'
            }
          }
        }
      }
    });
  }

  // Map visualization placeholder
  const mapContainer = document.getElementById('geo-spending-map');
  if (mapContainer) {
    mapContainer.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; height: 100%; color: var(--text-secondary);">' +
      '<p>Geographic visualization - loading data...</p>' +
      '</div>';
  }

  // Setup time period selector event
  const updateTimeChartsBtn = document.getElementById('update-time-charts');
  if (updateTimeChartsBtn) {
    updateTimeChartsBtn.addEventListener('click', updateTimeCharts);
  }
}

// Update time-based charts when period changes
function updateTimeCharts() {
  const period = document.getElementById('time-period').value;
  const days = parseInt(period);
  
  // Update labels based on selected period
  const labels = Array.from({length: days}, (_, i) => `Day ${i+1}`);
  
  // Fetch data for the selected period
  fetch(`/api/analytics/time-series?period=${days}`)
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      // Update charts with the new data
      if (window.timeTransactionsChart) {
        window.timeTransactionsChart.data.labels = labels;
        window.timeTransactionsChart.data.datasets[0].data = data.transactions || 
          Array.from({length: days}, () => Math.floor(Math.random() * 50) + 30); // Fallback to random
        window.timeTransactionsChart.update();
      }
      
      if (window.timeTransfersChart) {
        window.timeTransfersChart.data.labels = labels;
        window.timeTransfersChart.data.datasets[0].data = data.transfers || 
          Array.from({length: days}, () => Math.floor(Math.random() * 40) + 20); // Fallback to random
        window.timeTransfersChart.update();
      }
      
      console.log(`Charts updated for the last ${days} days with API data`);
    })
    .catch(error => {
      console.error('Error fetching time series data:', error);
      
      // Fallback to random data on error
      if (window.timeTransactionsChart) {
        window.timeTransactionsChart.data.labels = labels;
        window.timeTransactionsChart.data.datasets[0].data = 
          Array.from({length: days}, () => Math.floor(Math.random() * 50) + 30);
        window.timeTransactionsChart.update();
      }
      
      if (window.timeTransfersChart) {
        window.timeTransfersChart.data.labels = labels;
        window.timeTransfersChart.data.datasets[0].data = 
          Array.from({length: days}, () => Math.floor(Math.random() * 40) + 20);
        window.timeTransfersChart.update();
      }
      
      console.log(`Charts updated for the last ${days} days with random data (API error)`);
    });
}

// Fetch and update analytics data from the API
function fetchAnalyticsData() {
  // Update stat cards
  fetchSummaryStats();
  
  // Update charts
  fetchChartData();
  
  // Update tables
  fetchTableData();
}

// Fetch summary statistics
function fetchSummaryStats() {
  fetch('/api/summary')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      // Update summary cards
      updateSummaryCards(data);
    })
    .catch(error => {
      console.error('Error fetching summary data:', error);
    });
}

// Update summary cards with data
function updateSummaryCards(data) {
  // Find all stats cards
  const totalUsersEl = document.querySelector('.stats-card .stats-value:nth-of-type(1)');
  const totalTransfersEl = document.querySelector('.stats-card:nth-of-type(2) .stats-value');
  const avgTransferEl = document.querySelector('.stats-card:nth-of-type(3) .stats-value');
  const totalTransactionsEl = document.querySelector('.stats-card:nth-of-type(4) .stats-value');
  
  // User growth indicators
  const userGrowthEl = document.querySelector('.stats-card:nth-of-type(1) .stats-change');
  const transferGrowthEl = document.querySelector('.stats-card:nth-of-type(2) .stats-change');
  const avgTransferGrowthEl = document.querySelector('.stats-card:nth-of-type(3) .stats-change');
  const transactionGrowthEl = document.querySelector('.stats-card:nth-of-type(4) .stats-change');
  
  // Update values if elements exist and data is available
  if (totalUsersEl && data.total_users) {
    totalUsersEl.textContent = formatNumber(data.total_users);
  }
  
  if (totalTransfersEl && data.total_transfers) {
    totalTransfersEl.textContent = formatCurrency(data.total_transfers);
  }
  
  if (avgTransferEl && data.average_transfer) {
    avgTransferEl.textContent = formatCurrency(data.average_transfer);
  }
  
  if (totalTransactionsEl && data.total_transactions) {
    totalTransactionsEl.textContent = formatNumber(data.total_transactions);
  }
  
  // Update growth indicators
  updateGrowthIndicator(userGrowthEl, data.user_growth);
  updateGrowthIndicator(transferGrowthEl, data.transfer_growth);
  updateGrowthIndicator(avgTransferGrowthEl, data.avg_transfer_growth);
  updateGrowthIndicator(transactionGrowthEl, data.transaction_growth);
}

// Update growth indicator
function updateGrowthIndicator(element, value) {
  if (!element || value === undefined) return;
  
  // Determine if positive or negative
  const isPositive = value >= 0;
  const absValue = Math.abs(value);
  
  // Update class
  element.className = `stats-change ${isPositive ? 'positive' : 'negative'}`;
  
  // Update content
  element.innerHTML = `
    <i class="fas fa-arrow-${isPositive ? 'up' : 'down'}"></i> 
    ${absValue.toFixed(1)}% from last month
  `;
}

// Fetch chart data
function fetchChartData() {
  fetch('/api/analytics')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      // Update charts with the data
      updateCharts(data);
    })
    .catch(error => {
      console.error('Error fetching chart data:', error);
    });
}

// Update charts with API data
function updateCharts(data) {
  // Update spending distribution chart
  if (window.spendingDistributionChart && data.spending_distribution) {
    window.spendingDistributionChart.data.datasets[0].data = data.spending_distribution;
    window.spendingDistributionChart.update();
  }
  
  // Update transfer distribution chart
  if (window.transferDistributionChart && data.transfer_distribution) {
    window.transferDistributionChart.data.datasets[0].data = data.transfer_distribution;
    window.transferDistributionChart.update();
  }
  
  // Update popular items trend chart
  if (window.popularItemsTrendChart && data.popular_items) {
    data.popular_items.forEach((item, index) => {
      if (index < window.popularItemsTrendChart.data.datasets.length) {
        window.popularItemsTrendChart.data.datasets[index].data = item.monthly_data;
        window.popularItemsTrendChart.data.datasets[index].label = item.item;
      }
    });
    window.popularItemsTrendChart.update();
  }
  
  // Update time series charts (initial load)
  if (window.timeTransactionsChart && data.time_transactions) {
    window.timeTransactionsChart.data.labels = data.time_labels || window.timeTransactionsChart.data.labels;
    window.timeTransactionsChart.data.datasets[0].data = data.time_transactions;
    window.timeTransactionsChart.update();
  }
  
  if (window.timeTransfersChart && data.time_transfers) {
    window.timeTransfersChart.data.labels = data.time_labels || window.timeTransfersChart.data.labels;
    window.timeTransfersChart.data.datasets[0].data = data.time_transfers;
    window.timeTransfersChart.update();
  }
  
  // Update geographical data if available
  if (data.geo_data) {
    updateGeoVisualization(data.geo_data);
  }
}

// Update geographic visualization
function updateGeoVisualization(geoData) {
  const mapContainer = document.getElementById('geo-spending-map');
  if (!mapContainer) return;
  
  // If D3 is available, create a map visualization
  if (typeof d3 !== 'undefined') {
    mapContainer.innerHTML = ''; // Clear placeholder
    
    // This would be where you implement your D3 geographical visualization
    // For now, we'll just show the data is loaded
    mapContainer.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; height: 100%; color: var(--text-secondary);">' +
      '<p>Geographic data loaded successfully</p>' +
      '</div>';
  }
}

// Fetch table data
function fetchTableData() {
  // Fetch top spenders
  fetch('/api/users?sort=total_spent&limit=5')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      updateTopSpendersTable(data.data || []);
    })
    .catch(error => {
      console.error('Error fetching top spenders:', error);
    });
  
  // Fetch top transferers
  fetch('/api/transfers/summary?sort=volume&limit=5')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      updateTopTransferersTable(data.data || []);
    })
    .catch(error => {
      console.error('Error fetching top transferers:', error);
    });
}

// Update top spenders table
function updateTopSpendersTable(users) {
  const tableBody = document.querySelector('#top-spenders-table tbody');
  if (!tableBody) return;
  
  if (users.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No data available</td></tr>';
    return;
  }
  
  tableBody.innerHTML = '';
  
  users.forEach(user => {
    const row = document.createElement('tr');
    
    // Calculate average transaction
    const avgTransaction = user.transaction_count > 0 
      ? user.total_spent / user.transaction_count 
      : 0;
    
    row.innerHTML = `
      <td>${user.first_name || ''} ${user.last_name || ''}</td>
      <td>${user.email || ''}</td>
      <td>${formatCurrency(user.total_spent)}</td>
      <td>${formatCurrency(avgTransaction)}</td>
      <td>${formatNumber(user.transaction_count)}</td>
    `;
    
    tableBody.appendChild(row);
  });
}

// Update top transferers table
function updateTopTransferersTable(users) {
  const tableBody = document.querySelector('#top-transferers-table tbody');
  if (!tableBody) return;
  
  if (users.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No data available</td></tr>';
    return;
  }
  
  tableBody.innerHTML = '';
  
  users.forEach(user => {
    const row = document.createElement('tr');
    
    // Calculate total volume
    const totalVolume = (user.total_sent || 0) + (user.total_received || 0);
    
    row.innerHTML = `
      <td>${user.first_name || ''} ${user.last_name || ''}</td>
      <td>${user.email || ''}</td>
      <td>${formatCurrency(totalVolume)}</td>
      <td>${formatCurrency(user.total_sent)}</td>
      <td>${formatCurrency(user.total_received)}</td>
      <td>${formatNumber(user.transfer_count)}</td>
    `;
    
    tableBody.appendChild(row);
  });
}

// Format currency values with $ and thousands separators
function formatCurrency(value) {
  if (value === null || value === undefined) return '-';
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
}

// Format large numbers with thousands separators
function formatNumber(value) {
  if (value === null || value === undefined) return '-';
  
  return new Intl.NumberFormat('en-US').format(value);
}