/**
 * Dashboard JavaScript file for Venmito dashboard.
 * Manages the charts and data for the main dashboard page.
 */

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
    console.log("Dashboard loaded with dark theme");
    initializeCharts();
    loadDashboardData();
});

/**
 * Initialize chart instances with default settings
 */
function initializeCharts() {
    // Activity Chart
    const activityCtx = document.getElementById('activity-chart');
    if (activityCtx) {
        window.activityChart = new Chart(activityCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Transfers',
                    data: [8540, 9320, 8950, 10250, 10850, 11280, 12150, 12980, 13250, 14350, 15420, 15980],
                    borderColor: chartColors.blue,
                    backgroundColor: 'rgba(66, 133, 244, 0.1)',
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Transactions',
                    data: [3250, 3420, 3680, 3890, 4120, 4350, 4580, 4720, 4980, 5250, 5620, 5980],
                    borderColor: chartColors.green,
                    backgroundColor: 'rgba(52, 168, 83, 0.1)',
                    tension: 0.3,
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
                            text: 'Count'
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
                        text: 'Activity Over Time',
                        padding: {
                            top: 10,
                            bottom: 20
                        }
                    }
                }
            }
        });
    }

    // Sources Chart
    const sourcesCtx = document.getElementById('sources-chart');
    if (sourcesCtx) {
        window.sourcesChart = new Chart(sourcesCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['JSON', 'YAML', 'CSV', 'API'],
                datasets: [{
                    data: [40, 25, 20, 15],
                    backgroundColor: [
                        chartColors.blue, 
                        chartColors.green, 
                        chartColors.yellow, 
                        chartColors.red
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
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Data Source Distribution (%)',
                        padding: {
                            top: 10,
                            bottom: 20
                        }
                    }
                }
            }
        });
    }
}

/**
 * Load dashboard data from API
 */
async function loadDashboardData() {
    try {
        // Update summary cards
        fetchSummaryStats();
        
        // Update charts
        fetchChartData();
        
        // Update tables
        fetchTableData();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

/**
 * Fetch summary statistics from API
 */
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
            // Show error or use fallback data
        });
}

/**
 * Update summary cards with data
 * @param {Object} data - Summary statistics data
 */
function updateSummaryCards(data) {
    // Update each stats card if element exists and data is available
    const totalUsersEl = document.querySelector('.stats-card:nth-of-type(1) .stats-value');
    const totalTransfersEl = document.querySelector('.stats-card:nth-of-type(2) .stats-value');
    const avgTransferEl = document.querySelector('.stats-card:nth-of-type(3) .stats-value');
    const totalTransactionsEl = document.querySelector('.stats-card:nth-of-type(4) .stats-value');
    
    // Growth indicators
    const userGrowthEl = document.querySelector('.stats-card:nth-of-type(1) .stats-change');
    const transferGrowthEl = document.querySelector('.stats-card:nth-of-type(2) .stats-change');
    const avgTransferGrowthEl = document.querySelector('.stats-card:nth-of-type(3) .stats-change');
    const transactionGrowthEl = document.querySelector('.stats-card:nth-of-type(4) .stats-change');
    
    // Update values if elements exist and data is available
    if (totalUsersEl && data.total_users) {
        totalUsersEl.textContent = formatNumber(data.total_users);
    }
    
    if (totalTransfersEl && data.total_transfers) {
        totalTransfersEl.textContent = formatCurrency(data.total_transfers, false);
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

/**
 * Update growth indicator elements
 * @param {Element} element - Growth indicator element
 * @param {number} value - Growth percentage value
 */
function updateGrowthIndicator(element, value) {
    if (!element || value === undefined) return;
    
    // Determine if positive or negative
    const isPositive = value >= 0;
    const absValue = Math.abs(value);
    
    // Update class and content
    element.className = `stats-change ${isPositive ? 'positive' : 'negative'}`;
    element.innerHTML = `
        <i class="fas fa-arrow-${isPositive ? 'up' : 'down'}"></i> 
        ${absValue.toFixed(1)}% from last month
    `;
}

/**
 * Fetch chart data from API
 */
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

/**
 * Update charts with API data
 * @param {Object} data - Analytics data
 */
function updateCharts(data) {
    // Update activity chart
    if (window.activityChart && data.monthly_activity) {
        // Update monthly data
        window.activityChart.data.labels = data.monthly_activity.labels || 
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        if (data.monthly_activity.transfers) {
            window.activityChart.data.datasets[0].data = data.monthly_activity.transfers;
        }
        
        if (data.monthly_activity.transactions) {
            window.activityChart.data.datasets[1].data = data.monthly_activity.transactions;
        }
        
        window.activityChart.update();
    }
    
    // Update sources chart
    if (window.sourcesChart && data.data_sources) {
        window.sourcesChart.data.labels = data.data_sources.labels || 
            ['JSON', 'YAML', 'CSV', 'API'];
        window.sourcesChart.data.datasets[0].data = data.data_sources.values || 
            [40, 25, 20, 15];
        window.sourcesChart.update();
    }
}

/**
 * Fetch table data from API
 */
function fetchTableData() {
    // Fetch recent transfers
    fetch('/api/transfers?limit=3&sort=timestamp&order=desc')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            updateRecentTransfersTable(data.data || []);
        })
        .catch(error => {
            console.error('Error fetching recent transfers:', error);
        });
    
    // Fetch recent transactions
    fetch('/api/transactions?limit=3&sort=timestamp&order=desc')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            updateRecentTransactionsTable(data.data || []);
        })
        .catch(error => {
            console.error('Error fetching recent transactions:', error);
        });
}

/**
 * Update recent transfers table with API data
 * @param {Array} transfers - Recent transfers data
 */
function updateRecentTransfersTable(transfers) {
    const tableBody = document.querySelector('table:nth-of-type(1) tbody');
    if (!tableBody) return;
    
    if (transfers.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No recent transfers</td></tr>';
        return;
    }
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Fetch user details for each transfer if not included
    const userPromises = [];
    const userCache = {};
    
    // Collect unique user IDs that need to be fetched
    const userIds = new Set();
    transfers.forEach(transfer => {
        if (transfer.sender_id && !transfer.sender_name) {
            userIds.add(transfer.sender_id);
        }
        if (transfer.recipient_id && !transfer.recipient_name) {
            userIds.add(transfer.recipient_id);
        }
    });
    
    // If we need to fetch user details
    if (userIds.size > 0) {
        // Fetch user details for all unique user IDs
        userPromises.push(
            fetch(`/api/users?ids=${Array.from(userIds).join(',')}`)
                .then(response => response.json())
                .then(data => {
                    // Create a cache of user details
                    (data.data || []).forEach(user => {
                        userCache[user.user_id] = {
                            name: `${user.first_name} ${user.last_name}`,
                            email: user.email
                        };
                    });
                })
                .catch(error => {
                    console.error('Error fetching user details:', error);
                })
        );
    }
    
    // Once all user details are fetched, update the table
    Promise.all(userPromises).then(() => {
        transfers.forEach(transfer => {
            const row = document.createElement('tr');
            
            // Get sender name
            const senderName = transfer.sender_name || 
                (userCache[transfer.sender_id] ? userCache[transfer.sender_id].name : `User ${transfer.sender_id}`);
            
            // Get recipient name
            const recipientName = transfer.recipient_name || 
                (userCache[transfer.recipient_id] ? userCache[transfer.recipient_id].name : `User ${transfer.recipient_id}`);
            
            // Format date
            const date = new Date(transfer.timestamp);
            const formattedDate = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
            
            row.innerHTML = `
                <td>${senderName}</td>
                <td>${recipientName}</td>
                <td>${formatCurrency(transfer.amount)}</td>
                <td>${formattedDate}</td>
            `;
            
            tableBody.appendChild(row);
        });
    });
}

/**
 * Update recent transactions table with API data
 * @param {Array} transactions - Recent transactions data
 */
function updateRecentTransactionsTable(transactions) {
    const tableBody = document.querySelector('table:nth-of-type(2) tbody');
    if (!tableBody) return;
    
    if (transactions.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No recent transactions</td></tr>';
        return;
    }
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Fetch user details for each transaction if not included
    const userPromises = [];
    const userCache = {};
    
    // Collect unique user IDs that need to be fetched
    const userIds = new Set();
    transactions.forEach(transaction => {
        if (transaction.user_id && !transaction.user_name) {
            userIds.add(transaction.user_id);
        }
    });
    
    // If we need to fetch user details
    if (userIds.size > 0) {
        // Fetch user details for all unique user IDs
        userPromises.push(
            fetch(`/api/users?ids=${Array.from(userIds).join(',')}`)
                .then(response => response.json())
                .then(data => {
                    // Create a cache of user details
                    (data.data || []).forEach(user => {
                        userCache[user.user_id] = {
                            name: `${user.first_name} ${user.last_name}`,
                            email: user.email
                        };
                    });
                })
                .catch(error => {
                    console.error('Error fetching user details:', error);
                })
        );
    }
    
    // Once all user details are fetched, update the table
    Promise.all(userPromises).then(() => {
        transactions.forEach(transaction => {
            const row = document.createElement('tr');
            
            // Get user name
            const userName = transaction.user_name || 
                (userCache[transaction.user_id] ? userCache[transaction.user_id].name : `User ${transaction.user_id}`);
            
            row.innerHTML = `
                <td>${userName}</td>
                <td>${transaction.item}</td>
                <td>${transaction.store}</td>
                <td>${formatCurrency(transaction.price)}</td>
            `;
            
            tableBody.appendChild(row);
        });
    });
}

/**
 * Format currency values with $ and thousands separators
 * @param {number} value - The numeric value to format
 * @param {boolean} showCents - Whether to show cents
 * @returns {string} - Formatted currency string
 */
function formatCurrency(value, showCents = true) {
    if (value === null || value === undefined) return '-';
    
    const options = {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: showCents ? 2 : 0,
        maximumFractionDigits: showCents ? 2 : 0
    };
    
    return new Intl.NumberFormat('en-US', options).format(value);
}

/**
 * Format large numbers with thousands separators
 * @param {number} value - The numeric value to format
 * @returns {string} - Formatted number string
 */
function formatNumber(value) {
    if (value === null || value === undefined) return '-';
    
    return new Intl.NumberFormat('en-US').format(value);
}

