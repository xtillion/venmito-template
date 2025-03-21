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
        // Always start with mock data as a fallback
        updateWithMockData();
        
        // Then try to load from the real API
        fetchDashboardData();
        fetchTableData();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

/**
 * Update UI with mock data for development
 */
function updateWithMockData() {
    // Mock summary data
    const summaryData = {
        total_users: 2584,
        total_transfers: 487320,
        average_transfer: 78.42,
        total_transactions: 18237,
        user_growth: 12.5,
        transfer_growth: 8.3,
        avg_transfer_growth: -2.1,
        transaction_growth: 15.2
    };
    
    // Update summary cards
    updateSummaryCards(summaryData);
    
    // Mock analytics data
    const analyticsData = {
        monthly_activity: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            transfers: [8540, 9320, 8950, 10250, 10850, 11280, 12150, 12980, 13250, 14350, 15420, 15980],
            transactions: [3250, 3420, 3680, 3890, 4120, 4350, 4580, 4720, 4980, 5250, 5620, 5980]
        },
        data_sources: {
            labels: ['JSON', 'YAML', 'CSV', 'API'],
            values: [40, 25, 20, 15]
        }
    };
    
    // Update charts
    updateCharts(analyticsData);
    
    // Mock transfers data
    const transfersData = {
        data: [
            {
                transfer_id: 1,
                sender_id: 1,
                sender_name: 'John Doe',
                recipient_id: 2,
                recipient_name: 'Jane Smith',
                amount: 100.00,
                timestamp: '2023-01-15T12:30:45Z'
            },
            {
                transfer_id: 2,
                sender_id: 2,
                sender_name: 'Jane Smith',
                recipient_id: 3,
                recipient_name: 'Bob Johnson',
                amount: 50.25,
                timestamp: '2023-02-20T14:25:10Z'
            },
            {
                transfer_id: 3,
                sender_id: 3,
                sender_name: 'Bob Johnson',
                recipient_id: 1,
                recipient_name: 'John Doe',
                amount: 75.50,
                timestamp: '2023-03-25T09:15:30Z'
            }
        ]
    };
    
    // Update transfers table
    updateRecentTransfersTable(transfersData.data);
    
    // Mock transactions data
    const transactionsData = {
        data: [
            {
                transaction_id: 'T001',
                user_id: 1,
                user_name: 'John Doe',
                item: 'Laptop Computer',
                store: 'Electronics Store',
                price: 1200.00,
                timestamp: '2023-01-15T12:30:45Z'
            },
            {
                transaction_id: 'T002',
                user_id: 2,
                user_name: 'Jane Smith',
                item: 'Smartphone',
                store: 'Phone Shop',
                price: 800.00,
                timestamp: '2023-02-20T14:25:10Z'
            },
            {
                transaction_id: 'T003',
                user_id: 3,
                user_name: 'Bob Johnson',
                item: 'Wireless Headphones',
                store: 'Audio Outlet',
                price: 150.00,
                timestamp: '2023-03-25T09:15:30Z'
            }
        ]
    };
    
    // Update transactions table
    updateRecentTransactionsTable(transactionsData.data);
}

/**
 * Fetch main dashboard data from the API
 */
function fetchDashboardData() {
    // Fetch from the analytics/dashboard endpoint
    fetch('/api/analytics/dashboard')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Dashboard data received:', data);
            
            // Process the dashboard data to match the expected format
            processDashboardData(data);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            // Already using mock data as fallback
        });
}

/**
 * Process data from the analytics dashboard API and update the UI
 */
function processDashboardData(dashboardData) {
    // Extract data needed for summary cards
    if (dashboardData) {
        // Try to construct a summary object from the dashboard data
        const summaryData = {
            // These are placeholders - actual data depends on your API response structure
            total_users: dashboardData.user_count || 0,
            total_transfers: calculateTotalTransfers(dashboardData),
            average_transfer: calculateAverageTransfer(dashboardData),
            total_transactions: calculateTotalTransactions(dashboardData),
            user_growth: dashboardData.user_growth || 0,
            transfer_growth: dashboardData.transfer_growth || 0,
            avg_transfer_growth: dashboardData.avg_transfer_growth || 0,
            transaction_growth: dashboardData.transaction_growth || 0
        };
        
        // Update summary cards
        updateSummaryCards(summaryData);
        
        // Process daily transactions and transfers for the activity chart
        if (dashboardData.daily_transactions && dashboardData.daily_transfers) {
            const chartData = processTimeSeriesData(dashboardData.daily_transactions, dashboardData.daily_transfers);
            updateCharts(chartData);
        }
        
        // Update spending distribution data if available 
        if (dashboardData.spending_distribution) {
            updateSpendingDistribution(dashboardData.spending_distribution);
        }
        
        // Update top users tables if available
        if (dashboardData.top_users_by_spending) {
            updateTopUsersBySpending(dashboardData.top_users_by_spending);
        }
        
        if (dashboardData.top_users_by_transfers) {
            updateTopUsersByTransfers(dashboardData.top_users_by_transfers);
        }
    }
}

/**
 * Calculate total transfers from dashboard data
 */
function calculateTotalTransfers(data) {
    // Implement based on your actual API response structure
    if (data.daily_transfers && Array.isArray(data.daily_transfers.data)) {
        return data.daily_transfers.data.reduce((sum, day) => sum + day.count, 0);
    }
    return 0;
}

/**
 * Calculate average transfer from dashboard data
 */
function calculateAverageTransfer(data) {
    // Implement based on your actual API response structure
    if (data.transfer_distribution && Array.isArray(data.transfer_distribution.ranges)) {
        const totalAmount = data.transfer_distribution.ranges.reduce((sum, range) => sum + range.total_amount, 0);
        const totalCount = data.transfer_distribution.ranges.reduce((sum, range) => sum + range.count, 0);
        return totalCount > 0 ? totalAmount / totalCount : 0;
    }
    return 0;
}

/**
 * Calculate total transactions from dashboard data
 */
function calculateTotalTransactions(data) {
    // Implement based on your actual API response structure
    if (data.daily_transactions && Array.isArray(data.daily_transactions.data)) {
        return data.daily_transactions.data.reduce((sum, day) => sum + day.count, 0);
    }
    return 0;
}

/**
 * Process time series data from daily transactions and transfers
 */
function processTimeSeriesData(transactions, transfers) {
    // You'll need to adapt this to match your actual API response format
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    // Example function assuming your API returns daily data that needs to be aggregated
    const monthlyTransactions = Array(12).fill(0);
    const monthlyTransfers = Array(12).fill(0);
    
    // Process transactions data - assuming it contains date and count
    if (transactions.data && Array.isArray(transactions.data)) {
        transactions.data.forEach(day => {
            const date = new Date(day.date);
            const monthIndex = date.getMonth();
            monthlyTransactions[monthIndex] += day.count;
        });
    }
    
    // Process transfers data - assuming it contains date and count
    if (transfers.data && Array.isArray(transfers.data)) {
        transfers.data.forEach(day => {
            const date = new Date(day.date);
            const monthIndex = date.getMonth();
            monthlyTransfers[monthIndex] += day.count;
        });
    }
    
    return {
        monthly_activity: {
            labels: months,
            transfers: monthlyTransfers,
            transactions: monthlyTransactions
        }
    };
}

/**
 * Update spending distribution chart
 */
function updateSpendingDistribution(distribution) {
    // Assuming your sources chart is being used for spending distribution
    if (window.sourcesChart && distribution) {
        // Adapt to your actual API response format
        const labels = [];
        const values = [];
        
        // Process your distribution data
        // This is just an example - adjust based on your actual data structure
        if (Array.isArray(distribution.categories)) {
            distribution.categories.forEach(category => {
                labels.push(category.name);
                values.push(category.percentage);
            });
            
            window.sourcesChart.data.labels = labels;
            window.sourcesChart.data.datasets[0].data = values;
            window.sourcesChart.update();
        }
    }
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
    if (totalUsersEl && data.total_users !== undefined) {
        totalUsersEl.textContent = formatNumber(data.total_users);
    }
    
    if (totalTransfersEl && data.total_transfers !== undefined) {
        totalTransfersEl.textContent = formatCurrency(data.total_transfers, false);
    }
    
    if (avgTransferEl && data.average_transfer !== undefined) {
        avgTransferEl.textContent = formatCurrency(data.average_transfer);
    }
    
    if (totalTransactionsEl && data.total_transactions !== undefined) {
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
    // Fetch recent transfers - match your actual API endpoint
    fetch('/api/transfers?per_page=3')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(result => {
            // Check for expected data structure
            if (result && result.data && Array.isArray(result.data)) {
                updateRecentTransfersTable(result.data);
            }
        })
        .catch(error => {
            console.error('Error fetching recent transfers:', error);
            // Already using mock data as fallback
        });
    
    // Fetch recent transactions - match your actual API endpoint
    fetch('/api/transactions?per_page=3')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(result => {
            // Check for expected data structure
            if (result && result.data && Array.isArray(result.data)) {
                updateRecentTransactionsTable(result.data);
            }
        })
        .catch(error => {
            console.error('Error fetching recent transactions:', error);
            // Already using mock data as fallback
        });
}

/**
 * Update recent transfers table with API data
 * @param {Array} transfers - Recent transfers data
 */
function updateRecentTransfersTable(transfers) {
    const tableBody = document.querySelector('table:nth-of-type(1) tbody');
    if (!tableBody) return;
    
    if (!transfers || transfers.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No recent transfers</td></tr>';
        return;
    }
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Process transfers data to get sender and recipient names
    const processedTransfers = transfers.map(transfer => {
        // Your API might include sender_name and recipient_name directly
        // If not, you'll need to fetch user details separately
        return {
            ...transfer,
            sender_name: transfer.sender_name || `User ${transfer.sender_id}`,
            recipient_name: transfer.recipient_name || `User ${transfer.recipient_id}`
        };
    });
    
    // Create table rows
    processedTransfers.forEach(transfer => {
        const row = document.createElement('tr');
        
        // Format date
        const date = new Date(transfer.timestamp);
        const formattedDate = date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        row.innerHTML = `
            <td>${transfer.sender_name}</td>
            <td>${transfer.recipient_name}</td>
            <td>${formatCurrency(transfer.amount)}</td>
            <td>${formattedDate}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

/**
 * Update recent transactions table with API data
 * @param {Array} transactions - Recent transactions data
 */
function updateRecentTransactionsTable(transactions) {
    const tableBody = document.querySelector('table:nth-of-type(2) tbody');
    if (!tableBody) return;
    
    if (!transactions || transactions.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No recent transactions</td></tr>';
        return;
    }
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Process transactions data to get user names
    const processedTransactions = transactions.map(transaction => {
        // Your API might include user_name directly
        // If not, you'll need to fetch user details separately
        return {
            ...transaction,
            user_name: transaction.user_name || `User ${transaction.user_id}`
        };
    });
    
    // Create table rows
    processedTransactions.forEach(transaction => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${transaction.user_name}</td>
            <td>${transaction.item}</td>
            <td>${transaction.store}</td>
            <td>${formatCurrency(transaction.price)}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

/**
 * Update top users by spending table
 */
function updateTopUsersBySpending(users) {
    // Implement if there's a table for top spenders in your UI
    console.log("Top users by spending:", users);
}

/**
 * Update top users by transfers table
 */
function updateTopUsersByTransfers(users) {
    // Implement if there's a table for top transferers in your UI
    console.log("Top users by transfers:", users);
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

/**
 * Display an error message in a container
 * @param {string} message - Error message
 * @param {string} containerId - ID of container to display error
 */
function displayError(message, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = `
      <div class="alert alert-danger" role="alert">
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
      </div>
    `;
}