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

// Spending Distribution Chart
const spendingDistributionCtx = document.getElementById('spending-distribution-chart').getContext('2d');
const spendingDistributionChart = new Chart(spendingDistributionCtx, {
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

// Update charts when time period changes
document.getElementById('update-time-charts').addEventListener('click', function() {
  const period = document.getElementById('time-period').value;
  const days = parseInt(period);
  
  // Update labels based on selected period
  const labels = Array.from({length: days}, (_, i) => `Day ${i+1}`);
  
  // Generate new random data
  const transactionData = Array.from({length: days}, () => Math.floor(Math.random() * 50) + 30);
  const transferData = Array.from({length: days}, () => Math.floor(Math.random() * 40) + 20);
  
  // Update charts
  timeTransactionsChart.data.labels = labels;
  timeTransactionsChart.data.datasets[0].data = transactionData;
  timeTransactionsChart.update();
  
  timeTransfersChart.data.labels = labels;
  timeTransfersChart.data.datasets[0].data = transferData;
  timeTransfersChart.update();
  
  console.log(`Charts updated for the last ${days} days`);
});

// Simple D3.js map visualization (placeholder)
document.addEventListener('DOMContentLoaded', function() {
  const mapContainer = document.getElementById('geo-spending-map');
  
  if (!mapContainer) return;
  
  // Display placeholder message
  mapContainer.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; height: 100%; color: var(--text-secondary);">' +
    '<p>Geographic visualization will be connected to API data</p>' +
    '</div>';
  
  // In a real implementation, we would initialize a D3.js map here
  // with geographic data from the API
});

// API connection helpers
const API_ENDPOINTS = {
  USERS: '/api/users',
  TRANSFERS: '/api/transfers', 
  TRANSACTIONS: '/api/transactions',
  ANALYTICS: '/api/analytics',
  SUMMARY: '/api/summary'
};

/**
 * Fetch data from the API
 * @param {string} endpoint - API endpoint
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with response data
 */
async function fetchFromAPI(endpoint, params = {}) {
  try {
    // Build query string
    const queryString = Object.keys(params)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join('&');
    
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    // Return mock data as fallback
    return getMockData(endpoint);
  }
}

/**
 * Get mock data for development/fallback
 * @param {string} endpoint - API endpoint
 * @returns {Object} - Mock data
 */
function getMockData(endpoint) {
  console.log(`Returning mock data for ${endpoint}`);
  
  // Simple mock data based on endpoint
  const mockData = {
    [API_ENDPOINTS.USERS]: {
      data: Array.from({length: 10}, (_, i) => ({
        user_id: i + 1,
        name: `User ${i + 1}`,
        email: `user${i + 1}@example.com`,
        total_spent: Math.round(Math.random() * 5000 * 100) / 100,
        transaction_count: Math.floor(Math.random() * 50)
      }))
    },
    [API_ENDPOINTS.TRANSFERS]: {
      data: Array.from({length: 20}, (_, i) => ({
        transfer_id: i + 1,
        sender_id: Math.floor(Math.random() * 10) + 1,
        recipient_id: Math.floor(Math.random() * 10) + 1,
        amount: Math.round(Math.random() * 500 * 100) / 100,
        timestamp: new Date(Date.now() - Math.random() * 30 * 86400000).toISOString()
      }))
    },
    [API_ENDPOINTS.TRANSACTIONS]: {
      data: Array.from({length: 30}, (_, i) => ({
        transaction_id: i + 1,
        user_id: Math.floor(Math.random() * 10) + 1,
        item: ['Electronics', 'Clothing', 'Food', 'Entertainment'][Math.floor(Math.random() * 4)],
        amount: Math.round(Math.random() * 200 * 100) / 100,
        timestamp: new Date(Date.now() - Math.random() * 30 * 86400000).toISOString()
      }))
    },
    [API_ENDPOINTS.ANALYTICS]: {
      spending_distribution: [35, 15, 20, 10, 12, 8],
      transfer_distribution: [382, 724, 516, 298, 157, 84],
      popular_items: [
        {
          item: 'Electronics',
          monthly_data: [42, 45, 38, 40, 48, 52, 54, 59, 63, 58, 65, 72]
        },
        {
          item: 'Clothing',
          monthly_data: [28, 30, 34, 32, 36, 39, 35, 38, 40, 42, 46, 51]
        },
        {
          item: 'Food & Dining',
          monthly_data: [35, 36, 37, 38, 40, 42, 44, 46, 48, 49, 50, 52]
        },
        {
          item: 'Entertainment',
          monthly_data: [22, 24, 26, 28, 30, 33, 35, 37, 38, 40, 42, 45]
        }
      ]
    },
    [API_ENDPOINTS.SUMMARY]: {
      total_users: 2584,
      total_transfers: 487320,
      average_transfer: 78.42,
      total_transactions: 18237,
      user_growth: 12.5,
      transfer_growth: 8.3,
      avg_transfer_growth: -2.1,
      transaction_growth: 15.2
    }
  };
  
  return mockData[endpoint] || { data: [] };
}

// Initialize with mock data for now, can be replaced with actual API calls
// in production by uncommenting the API calls below
/*
// Fetch summary data
fetchFromAPI(API_ENDPOINTS.SUMMARY).then(data => {
  // Update summary cards with actual data
  // ...
});

// Fetch analytics data for charts
fetchFromAPI(API_ENDPOINTS.ANALYTICS).then(data => {
  // Update charts with actual data
  // ...
});

// Fetch top spenders
fetchFromAPI(API_ENDPOINTS.USERS, { sort: 'total_spent', limit: 5 }).then(data => {
  // Update top spenders table
  // ...
});

// Fetch top transferers
fetchFromAPI(API_ENDPOINTS.TRANSFERS, { group_by: 'user', sort: 'volume', limit: 5 }).then(data => {
  // Update top transferers table
  // ...
});
*/AspectRatio: false,
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

// Transfer Distribution Chart
const transferDistributionCtx = document.getElementById('transfer-distribution-chart').getContext('2d');
const transferDistributionChart = new Chart(transferDistributionCtx, {
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

// Popular Items Trend Chart
const popularItemsTrendCtx = document.getElementById('popular-items-trend-chart').getContext('2d');
const popularItemsTrendChart = new Chart(popularItemsTrendCtx, {
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

// Time Transactions Chart
const timeTransactionsCtx = document.getElementById('time-transactions-chart').getContext('2d');
const timeTransactionsChart = new Chart(timeTransactionsCtx, {
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

// Time Transfers Chart
const timeTransfersCtx = document.getElementById('time-transfers-chart').getContext('2d');
const timeTransfersChart = new Chart(timeTransfersCtx, {
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
    maintain