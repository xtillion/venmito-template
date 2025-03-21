/**
 * Users JavaScript for Venmito
 * 
 * This file handles the users page functionality, including:
 * - Loading and displaying users list
 * - Handling pagination
 * - Displaying user details in modals
 * - Searching and filtering users
 */

// Store current page state
const state = {
    currentPage: 1,
    perPage: 20,
    searchTerm: '',
    users: []
  };
  
  document.addEventListener('DOMContentLoaded', async () => {
    // Set up event listeners
    setupEventListeners();
    
    // Load initial users data
    await loadUsers();
  });
  
  /**
   * Set up event listeners for the page
   */
  function setupEventListeners() {
    // Search button click
    document.getElementById('search-btn')?.addEventListener('click', () => {
      state.searchTerm = document.getElementById('user-search').value;
      state.currentPage = 1; // Reset to first page when searching
      loadUsers();
    });
    
    // Search input enter key
    document.getElementById('user-search')?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        state.searchTerm = e.target.value;
        state.currentPage = 1; // Reset to first page when searching
        loadUsers();
      }
    });
    
    // Modal view full details button
    document.getElementById('view-user-details')?.addEventListener('click', () => {
      const userId = document.getElementById('user-details-btn')?.dataset.userId;
      if (userId) {
        window.location.href = `/people/${userId}`;
      }
    });
  }
  
  /**
   * Load users data from API with pagination and search
   */
  async function loadUsers() {
    try {
      const usersTable = document.getElementById('users-table');
      const tableBody = usersTable?.querySelector('tbody');
      
      if (tableBody) {
        // Show loading state
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center">Loading users...</td></tr>';
        
        // Fetch users data from API
        const response = await API.people.getUsers(state.currentPage, state.perPage, state.searchTerm);
        
        // Update state with users data
        state.users = response.data;
        
        // Render users table
        renderUsersTable(response.data);
        
        // Render pagination
        API.renderPagination(response.pagination, (page) => {
          state.currentPage = page;
          loadUsers();
        }, 'users-pagination');
      }
    } catch (error) {
      console.error('Error loading users:', error);
      // Error handling is managed by the API utility
    }
  }
  
  /**
   * Render users table with the provided data
   * 
   * @param {Array} users - Users data from API
   */
  function renderUsersTable(users) {
    const tableBody = document.getElementById('users-table')?.querySelector('tbody');
    
    if (!tableBody) return;
    
    if (users.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No users found</td></tr>';
      return;
    }
    
    tableBody.innerHTML = users.map(user => `
      <tr>
        <td>${user.user_id}</td>
        <td>${user.first_name} ${user.last_name}</td>
        <td>${user.email}</td>
        <td>${user.city ? user.city : ''}, ${user.country ? user.country : ''}</td>
        <td>
          <button class="btn btn-sm btn-primary view-user-btn" data-user-id="${user.user_id}" data-bs-toggle="modal" data-bs-target="#userModal">
            View
          </button>
        </td>
      </tr>
    `).join('');
    
    // Add event listeners for view buttons
    tableBody.querySelectorAll('.view-user-btn').forEach(button => {
      button.addEventListener('click', () => {
        const userId = button.dataset.userId;
        loadUserDetails(userId);
      });
    });
  }
  
  /**
   * Load user details for the modal
   * 
   * @param {string} userId - User ID to load details for
   */
  async function loadUserDetails(userId) {
    try {
      // Get user details
      const user = await API.people.getUser(userId);
      
      if (!user) {
        API.showError('User not found');
        return;
      }
      
      // Get user transaction summary
      const transactionSummary = await API.transactions.getUserTransactionsSummary(userId);
      
      // Get user transfer summary
      const transferSummary = await API.transfers.getUserTransfersSummary(userId);
      
      // Update modal with user details
      document.getElementById('user-name').textContent = `${user.first_name} ${user.last_name}`;
      document.getElementById('user-email').textContent = user.email || 'N/A';
      document.getElementById('user-phone').textContent = user.phone || 'N/A';
      document.getElementById('user-location').textContent = `${user.city || ''}, ${user.country || ''}`;
      document.getElementById('user-devices').textContent = user.devices || 'N/A';
      
      // Update transaction summary
      document.getElementById('user-total-spent').textContent = transactionSummary?.total_spent?.toFixed(2) || '0.00';
      document.getElementById('user-transaction-count').textContent = transactionSummary?.transaction_count || '0';
      document.getElementById('user-favorite-store').textContent = transactionSummary?.favorite_store || 'N/A';
      document.getElementById('user-favorite-item').textContent = transactionSummary?.favorite_item || 'N/A';
      
      // Update transfer summary
      document.getElementById('user-total-sent').textContent = transferSummary?.total_sent?.toFixed(2) || '0.00';
      document.getElementById('user-total-received').textContent = transferSummary?.total_received?.toFixed(2) || '0.00';
      document.getElementById('user-net-transferred').textContent = transferSummary?.net_transferred?.toFixed(2) || '0.00';
      document.getElementById('user-transfer-count').textContent = transferSummary?.transfer_count || '0';
      
      // Update view details button
      document.getElementById('view-user-details').dataset.userId = userId;
      
    } catch (error) {
      console.error('Error loading user details:', error);
      // Error handling is managed by the API utility
    }
  }