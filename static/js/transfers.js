/**
 * Transfers JavaScript for Venmito
 * 
 * This file handles the transfers page functionality, including:
 * - Loading and displaying transfers list
 * - Handling pagination
 * - Displaying transfer details in modals
 * - Filtering transfers by date range
 * - Rendering charts for transfer data
 */

// Store current page state
const state = {
  currentPage: 1,
  perPage: 20,
  filters: {
    userId: null,
    startDate: null,
    endDate: null
  },
  transfers: []
};

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize charts with loading state
  initializeCharts();
  
  // Set up event listeners
  setupEventListeners();
  
  // Load initial transfers data
  await loadTransfers();
  
  // Load chart data
  await loadChartData();
});

/**
 * Initialize charts with loading state
 */
function initializeCharts() {
  // Create empty transfer distribution chart
  const transferDistributionCtx = document.getElementById('transfer-distribution-chart');
  if (transferDistributionCtx) {
    window.transferDistributionChart = new Chart(transferDistributionCtx, {
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
  
  // Create empty daily transfers chart
  const dailyTransfersCtx = document.getElementById('daily-transfers-chart');
  if (dailyTransfersCtx) {
    window.dailyTransfersChart = new Chart(dailyTransfersCtx, {
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
            text: 'Loading daily transfers...'
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
  // Filter button click
  document.getElementById('filter-btn')?.addEventListener('click', () => {
    // Get filter values
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const searchTerm = document.getElementById('transfer-search').value;
    
    // Update state with filter values
    state.filters.startDate = startDate || null;
    state.filters.endDate = endDate || null;
    state.filters.userId = searchTerm ? parseInt(searchTerm) : null;
    state.currentPage = 1; // Reset to first page when filtering
    
    // Reload transfers with new filters
    loadTransfers();
  });
}

/**
 * Load transfers data from API with pagination and filters
 */
async function loadTransfers() {
  try {
    const transfersTable = document.getElementById('transfers-table');
    const tableBody = transfersTable?.querySelector('tbody');
    
    if (tableBody) {
      // Show loading state
      tableBody.innerHTML = '<tr><td colspan="6" class="text-center">Loading transfers...</td></tr>';
      
      // Fetch transfers data from API
      const response = await API.transfers.getTransfers(state.currentPage, state.perPage, state.filters);
      
      // Update state with transfers data
      state.transfers = response.data;
      
      // Render transfers table
      renderTransfersTable(response.data);
      
      // Render pagination
      API.renderPagination(response.pagination, (page) => {
        state.currentPage = page;
        loadTransfers();
      }, 'transfers-pagination');
    }
  } catch (error) {
    console.error('Error loading transfers:', error);
    // Error handling is managed by the API utility
  }
}

/**
 * Load chart data from API
 */
async function loadChartData() {
  try {
    // Load transfer distribution data
    const transferDistribution = await API.analytics.getTransferAmountDistribution();
    updateTransferDistributionChart(transferDistribution);
    
    // Load daily transfers data
    const dailyTransfers = await API.analytics.getDailyTransfersSummary(30);
    updateDailyTransfersChart(dailyTransfers);
  } catch (error) {
    console.error('Error loading chart data:', error);
    // Error handling is managed by the API utility
  }
}

/**
 * Update transfer distribution chart with data
 * 
 * @param {Array} data - Transfer distribution data
 */
function updateTransferDistributionChart(data) {
  if (!window.transferDistributionChart || !data || data.length === 0) return;
  
  // Format data for chart
  const labels = data.map(item => item.range);
  const counts = data.map(item => item.count);
  
  // Update chart data
  window.transferDistributionChart.data.labels = labels;
  window.transferDistributionChart.data.datasets[0].data = counts;
  window.transferDistributionChart.options.plugins.title.text = 'Transfer Amount Distribution';
  window.transferDistributionChart.update();
}

/**
 * Update daily transfers chart with data
 * 
 * @param {Array} data - Daily transfers data
 */
function updateDailyTransfersChart(data) {
  if (!window.dailyTransfersChart || !data || data.length === 0) return;
  
  // Format data for chart
  const labels = data.map(item => API.formatDate(item.date));
  const amounts = data.map(item => item.amount);
  
  // Update chart data
  window.dailyTransfersChart.data.labels = labels;
  window.dailyTransfersChart.data.datasets[0].data = amounts;
  window.dailyTransfersChart.options.plugins.title.text = 'Daily Transfer Volume (Last 30 Days)';
  window.dailyTransfersChart.update();
}

/**
 * Render transfers table with the provided data
 * 
 * @param {Array} transfers - Transfers data from API
 */
function renderTransfersTable(transfers) {
  const tableBody = document.getElementById('transfers-table')?.querySelector('tbody');
  
  if (!tableBody) return;
  
  if (transfers.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No transfers found</td></tr>';
    return;
  }
  
  tableBody.innerHTML = transfers.map(transfer => `
    <tr>
      <td>${transfer.transfer_id}</td>
      <td>${API.formatDateTime(transfer.timestamp)}</td>
      <td>${transfer.sender_name || `User #${transfer.sender_id}`}</td>
      <td>${transfer.recipient_name || `User #${transfer.recipient_id}`}</td>
      <td>${API.formatCurrency(transfer.amount)}</td>
      <td>
        <button class="btn btn-sm btn-primary view-transfer-btn" 
                data-transfer-id="${transfer.transfer_id}" 
                data-bs-toggle="modal" 
                data-bs-target="#transferModal">
          View
        </button>
      </td>
    </tr>
  `).join('');
  
  // Add event listeners for view buttons
  tableBody.querySelectorAll('.view-transfer-btn').forEach(button => {
    button.addEventListener('click', () => {
      const transferId = button.dataset.transferId;
      loadTransferDetails(transferId);
    });
  });
}

/**
 * Load transfer details for the modal
 * 
 * @param {string} transferId - Transfer ID to load details for
 */
async function loadTransferDetails(transferId) {
  try {
    // Get transfer details
    const transfer = await API.transfers.getTransfer(transferId);
    
    if (!transfer) {
      API.showError('Transfer not found');
      return;
    }
    
    // Get sender details
    const sender = await API.people.getUser(transfer.sender_id);
    
    // Get recipient details
    const recipient = await API.people.getUser(transfer.recipient_id);
    
    // Update modal with transfer details
    document.getElementById('transfer-id').textContent = transfer.transfer_id;
    document.getElementById('transfer-date').textContent = API.formatDateTime(transfer.timestamp);
    
    // Ensure amount is a number before using toFixed
    const amount = typeof transfer.amount === 'string' ? parseFloat(transfer.amount) : transfer.amount;
    document.getElementById('transfer-amount').textContent = amount.toFixed(2);
    
    // Update sender details
    document.getElementById('sender-name').textContent = sender ? `${sender.first_name} ${sender.last_name}` : `User #${transfer.sender_id}`;
    document.getElementById('sender-email').textContent = sender ? sender.email : 'N/A';
    document.getElementById('sender-details-link').href = `/people/${transfer.sender_id}`;
    
    // Update recipient details
    document.getElementById('recipient-name').textContent = recipient ? `${recipient.first_name} ${recipient.last_name}` : `User #${transfer.recipient_id}`;
    document.getElementById('recipient-email').textContent = recipient ? recipient.email : 'N/A';
    document.getElementById('recipient-details-link').href = `/people/${transfer.recipient_id}`;
    
  } catch (error) {
    console.error('Error loading transfer details:', error);
    // Error handling is managed by the API utility
  }
}