/**
 * Users JavaScript for Venmito
 * 
 * This file handles the users page functionality, including:
 * - Loading and displaying users list
 * - Handling pagination
 * - Displaying user details in modals
 * - Searching users
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize state
  const state = {
      currentPage: 1,
      perPage: 20,
      searchTerm: ''
  };

  // Set up event listeners
  setupEventListeners();
  
  // Load initial users data
  await loadUsers();

  /**
   * Set up event listeners for the page
   */
  function setupEventListeners() {
      // Search button
      const searchBtn = document.getElementById('search-btn');
      const searchInput = document.getElementById('user-search');

      if (searchBtn) {
          searchBtn.addEventListener('click', performSearch);
      }

      if (searchInput) {
          searchInput.addEventListener('keypress', (e) => {
              if (e.key === 'Enter') {
                  performSearch();
              }
          });
      }

      // View Full Details Button in Modal
      const viewDetailsBtn = document.getElementById('view-user-details');
      if (viewDetailsBtn) {
          viewDetailsBtn.addEventListener('click', () => {
              const userId = viewDetailsBtn.dataset.userId;
              if (userId) {
                  window.location.href = `/people/${userId}`;
              }
          });
      }
  }

  /**
   * Perform search based on search input
   */
  function performSearch() {
      const searchInput = document.getElementById('user-search');
      state.searchTerm = searchInput ? searchInput.value.trim() : '';
      state.currentPage = 1;
      loadUsers();
  }

  /**
   * Load users data from API
   */
  async function loadUsers() {
      try {
          const tableBody = document.querySelector('#users-table tbody');
          
          if (tableBody) {
              // Show loading state
              tableBody.innerHTML = `
                  <tr>
                      <td colspan="5" class="text-center">
                          <div class="spinner-border text-primary" role="status">
                              <span class="visually-hidden">Loading...</span>
                          </div>
                          Loading users...
                      </td>
                  </tr>
              `;

              // Fetch users from API
              const response = await window.API.people.getUsers(
                  state.currentPage, 
                  state.perPage, 
                  state.searchTerm
              );

              // Render users table
              renderUsersTable(response.data);

              // Render pagination
              renderPagination(response.pagination);
          }
      } catch (error) {
          console.error('Error loading users:', error);
          handleLoadError();
      }
  }

  /**
   * Render users table with provided data
   * @param {Array} users - Array of user objects
   */
  function renderUsersTable(users) {
      const tableBody = document.querySelector('#users-table tbody');
      
      if (!tableBody) return;

      if (!users || users.length === 0) {
          tableBody.innerHTML = `
              <tr>
                  <td colspan="5" class="text-center">No users found</td>
              </tr>
          `;
          return;
      }

      tableBody.innerHTML = users.map(user => `
          <tr>
              <td>${user.user_id || 'N/A'}</td>
              <td>${user.first_name || ''} ${user.last_name || ''}</td>
              <td>${user.email || 'N/A'}</td>
              <td>${user.city || ''}, ${user.country || ''}</td>
              <td>
                  <button 
                      class="btn btn-sm btn-primary view-user-btn" 
                      data-user-id="${user.user_id}"
                      data-bs-toggle="modal" 
                      data-bs-target="#userModal"
                  >
                      View
                  </button>
              </td>
          </tr>
      `).join('');

      // Add event listeners to view buttons
      document.querySelectorAll('.view-user-btn').forEach(button => {
          button.addEventListener('click', () => loadUserDetails(button.dataset.userId));
      });
  }

  /**
   * Render pagination controls
   * @param {Object} pagination - Pagination metadata
   */
  function renderPagination(pagination) {
      const paginationContainer = document.getElementById('users-pagination');
      
      if (!paginationContainer) return;

      const { current_page, total_pages, total } = pagination;

      // Clear existing pagination
      paginationContainer.innerHTML = '';

      // Previous button
      const prevLi = document.createElement('li');
      prevLi.className = `page-item ${current_page === 1 ? 'disabled' : ''}`;
      prevLi.innerHTML = `<a class="page-link" href="#" data-page="${current_page - 1}">Previous</a>`;
      paginationContainer.appendChild(prevLi);

      // Page numbers
      for (let i = 1; i <= total_pages; i++) {
          const pageLi = document.createElement('li');
          pageLi.className = `page-item ${i === current_page ? 'active' : ''}`;
          pageLi.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
          paginationContainer.appendChild(pageLi);
      }

      // Next button
      const nextLi = document.createElement('li');
      nextLi.className = `page-item ${current_page === total_pages ? 'disabled' : ''}`;
      nextLi.innerHTML = `<a class="page-link" href="#" data-page="${current_page + 1}">Next</a>`;
      paginationContainer.appendChild(nextLi);

      // Add click event listeners to pagination links
      paginationContainer.addEventListener('click', (e) => {
          const pageLink = e.target.closest('.page-link');
          if (pageLink && !pageLink.closest('.disabled')) {
              const page = parseInt(pageLink.dataset.page);
              state.currentPage = page;
              loadUsers();
          }
      });
  }

  /**
   * Load user details for modal
   * @param {string} userId - User ID to load details for
   */
  async function loadUserDetails(userId) {
      try {
          // Fetch user details
          const user = await window.API.people.getUser(userId);
          const transactionSummary = await window.API.transactions.getUserTransactionsSummary(userId);
          const transferSummary = await window.API.transfers.getUserTransfersSummary(userId);

          // Update modal with user details
          document.getElementById('user-name').textContent = `${user.first_name} ${user.last_name}`;
          document.getElementById('user-email').textContent = user.email || 'N/A';
          document.getElementById('user-phone').textContent = user.phone || 'N/A';
          document.getElementById('user-location').textContent = `${user.city || ''}, ${user.country || ''}`;
          document.getElementById('user-devices').textContent = user.devices || 'N/A';

          // Update transaction summary
          document.getElementById('user-total-spent').textContent = (transactionSummary?.total_spent || 0).toFixed(2);
          document.getElementById('user-transaction-count').textContent = transactionSummary?.transaction_count || 0;
          document.getElementById('user-favorite-store').textContent = transactionSummary?.favorite_store || 'N/A';
          document.getElementById('user-favorite-item').textContent = transactionSummary?.favorite_item || 'N/A';

          // Update transfer summary
          document.getElementById('user-total-sent').textContent = (transferSummary?.total_sent || 0).toFixed(2);
          document.getElementById('user-total-received').textContent = (transferSummary?.total_received || 0).toFixed(2);
          document.getElementById('user-net-transferred').textContent = (transferSummary?.net_transferred || 0).toFixed(2);
          document.getElementById('user-transfer-count').textContent = transferSummary?.transfer_count || 0;

          // Update view details button
          const viewDetailsBtn = document.getElementById('view-user-details');
          viewDetailsBtn.dataset.userId = userId;

      } catch (error) {
          console.error('Error loading user details:', error);
          // Optionally show an error message in the modal
      }
  }

  /**
   * Handle errors when loading users
   */
  function handleLoadError() {
      const tableBody = document.querySelector('#users-table tbody');
      if (tableBody) {
          tableBody.innerHTML = `
              <tr>
                  <td colspan="5" class="text-center text-danger">
                      Failed to load users. Please try again later.
                  </td>
              </tr>
          `;
      }
  }
});