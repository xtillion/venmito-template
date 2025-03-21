// Dashboard JavaScript
document.addEventListener("DOMContentLoaded", function() {
    console.log("Dashboard loaded");
    
    // Example fetch for data
    // fetch("/api/user-analytics")
    //     .then(response => response.json())
    //     .then(data => {
    //         // Process and visualize data
    //     });
});/**
* Dashboard JavaScript file for Venmito dashboard.
* Manages the charts and data for the main dashboard page.
*/

document.addEventListener('DOMContentLoaded', function() {
   loadDashboardData();
   setupCharts();
});

/**
* Load dashboard data from API
*/
async function loadDashboardData() {
   try {
       // Get dashboard data
       const dashboardData = await Utils.fetchAPI('/analytics/dashboard');
       
       // Update cards with summary statistics
       updateSummaryCards(dashboardData);
       
       // Update charts with data
       updateCharts(dashboardData);
       
       // Update top users table
       updateTopUsersTable(dashboardData.top_users_by_spending);
       
   } catch (error) {
       console.error('Error loading dashboard data:', error);
       alert('Failed to load dashboard data. Please try again later.');
   }
}

/**
* Update summary cards with data
* @param {Object} data - Dashboard data
*/
function updateSummaryCards(data) {
   // For now, we'll use mock data
   // In a real implementation, this would be replaced with the actual data
   
   // Total users
   const totalUsers = 1250;
   document.getElementById('total-users').textContent = totalUsers.toLocaleString();
   
   // Total transfers
   const totalTransfers = 8765;
   document.getElementById('total-transfers').textContent = totalTransfers.toLocaleString();
   
   // Total transactions
   const totalTransactions = 15420;
   document.getElementById('total-transactions').textContent = totalTransactions.toLocaleString();
   
   // Total revenue
   const totalRevenue = 975652.75;
   document.getElementById('total-revenue').textContent = Utils.formatCurrency(totalRevenue).replace('$', '');
}

/**
* Set up chart instances
*/
function setupCharts() {
   // Transfers chart
   const transfersCtx = document.getElementById('transfers-chart').getContext('2d');
   window.transfersChart = new Chart(transfersCtx, {
       type: 'line',
       data: {
           labels: [], // Will be populated with dates
           datasets: [{
               label: 'Transfer Count',
               data: [],
               borderColor: 'rgb(54, 162, 235)',
               backgroundColor: 'rgba(54, 162, 235, 0.1)',
               borderWidth: 2,
               tension: 0.2,
               fill: true
           }, {
               label: 'Transfer Amount',
               data: [],
               borderColor: 'rgb(75, 192, 192)',
               backgroundColor: 'rgba(75, 192, 192, 0.1)',
               borderWidth: 2,
               tension: 0.2,
               fill: true,
               yAxisID: 'y1'
           }]
       },
       options: {
           responsive: true,
           interaction: {
               mode: 'index',
               intersect: false,
           },
           scales: {
               y: {
                   title: {
                       display: true,
                       text: 'Transfer Count'
                   }
               },
               y1: {
                   position: 'right',
                   title: {
                       display: true,
                       text: 'Amount'
                   },
                   grid: {
                       drawOnChartArea: false,
                   },
               }
           }
       }
   });
   
   // Transactions chart
   const transactionsCtx = document.getElementById('transactions-chart').getContext('2d');
   window.transactionsChart = new Chart(transactionsCtx, {
       type: 'line',
       data: {
           labels: [], // Will be populated with dates
           datasets: [{
               label: 'Transaction Count',
               data: [],
               borderColor: 'rgb(255, 99, 132)',
               backgroundColor: 'rgba(255, 99, 132, 0.1)',
               borderWidth: 2,
               tension: 0.2,
               fill: true
           }, {
               label: 'Revenue',
               data: [],
               borderColor: 'rgb(255, 159, 64)',
               backgroundColor: 'rgba(255, 159, 64, 0.1)',
               borderWidth: 2,
               tension: 0.2,
               fill: true,
               yAxisID: 'y1'
           }]
       },
       options: {
           responsive: true,
           interaction: {
               mode: 'index',
               intersect: false,
           },
           scales: {
               y: {
                   title: {
                       display: true,
                       text: 'Transaction Count'
                   }
               },
               y1: {
                   position: 'right',
                   title: {
                       display: true,
                       text: 'Revenue'
                   },
                   grid: {
                       drawOnChartArea: false,
                   },
               }
           }
       }
   });
   
   // Spending distribution chart
   const spendingDistCtx = document.getElementById('spending-distribution-chart').getContext('2d');
   window.spendingDistChart = new Chart(spendingDistCtx, {
       type: 'pie',
       data: {
           labels: [], // Will be populated
           datasets: [{
               data: [],
               backgroundColor: Utils.generateChartColors(6)
           }]
       },
       options: {
           responsive: true,
           plugins: {
               legend: {
                   position: 'bottom'
               },
               tooltip: {
                   callbacks: {
                       label: function(context) {
                           const label = context.label || '';
                           const value = context.raw || 0;
                           const percentage = context.parsed || 0;
                           return `${label}: ${value} users (${percentage.toFixed(1)}%)`;
                       }
                   }
               }
           }
       }
   });
}

/**
* Update charts with data
* @param {Object} data - Dashboard data
*/
function updateCharts(data) {
   // For now, we'll use mock data
   // In a real implementation, this would be replaced with the actual data
   
   // Mock data for transfers chart
   const transfersDates = Array.from({length: 30}, (_, i) => {
       const date = new Date();
       date.setDate(date.getDate() - 29 + i);
       return date.toISOString().split('T')[0];
   });
   
   const transfersCount = Array.from({length: 30}, () => Math.floor(Math.random() * 100) + 50);
   const transfersAmount = Array.from({length: 30}, () => Math.floor(Math.random() * 10000) + 5000);
   
   // Update transfers chart
   window.transfersChart.data.labels = transfersDates;
   window.transfersChart.data.datasets[0].data = transfersCount;
   window.transfersChart.data.datasets[1].data = transfersAmount;
   window.transfersChart.update();
   
   // Mock data for transactions chart
   const transactionsDates = transfersDates; // Same dates
   const transactionsCount = Array.from({length: 30}, () => Math.floor(Math.random() * 150) + 30);
   const transactionsRevenue = Array.from({length: 30}, () => Math.floor(Math.random() * 15000) + 3000);
   
   // Update transactions chart
   window.transactionsChart.data.labels = transactionsDates;
   window.transactionsChart.data.datasets[0].data = transactionsCount;
   window.transactionsChart.data.datasets[1].data = transactionsRevenue;
   window.transactionsChart.update();
   
   // Mock data for spending distribution
   const spendingLabels = [
       '$0 (No purchases)', 
       '$0.01 - $99.99', 
       '$100 - $499.99',
       '$500 - $999.99',
       '$1,000 - $4,999.99',
       '$5,000+'
   ];
   const spendingData = [250, 450, 300, 150, 75, 25];
   
   // Update spending distribution chart
   window.spendingDistChart.data.labels = spendingLabels;
   window.spendingDistChart.data.datasets[0].data = spendingData;
   window.spendingDistChart.update();
}

/**
* Update top users table
* @param {Array} users - Top users by spending
*/
function updateTopUsersTable(users) {
   // For now, we'll use mock data
   // In a real implementation, this would be replaced with the actual data
   
   const mockUsers = [
       { first_name: 'John', last_name: 'Doe', total_spent: 15789.50, transaction_count: 42 },
       { first_name: 'Jane', last_name: 'Smith', total_spent: 12450.75, transaction_count: 36 },
       { first_name: 'Robert', last_name: 'Johnson', total_spent: 9876.25, transaction_count: 28 },
       { first_name: 'Emily', last_name: 'Wilson', total_spent: 8765.40, transaction_count: 31 },
       { first_name: 'Michael', last_name: 'Brown', total_spent: 7890.15, transaction_count: 25 }
   ];
   
   const tableBody = document.querySelector('#top-users-table tbody');
   tableBody.innerHTML = '';
   
   mockUsers.forEach(user => {
       const avgTransaction = user.total_spent / user.transaction_count;
       
       const row = document.createElement('tr');
       row.innerHTML = `
           <td>${user.first_name} ${user.last_name}</td>
           <td>${Utils.formatCurrency(user.total_spent)}</td>
           <td>${user.transaction_count}</td>
       `;
       
       tableBody.appendChild(row);
   });
}