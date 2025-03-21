/**
 * API Utilities for Venmito
 * Provides consistent API interaction methods across the application
 */

// API Base URL - change if your API is hosted elsewhere
const API_BASE_URL = '';

// API Endpoints
const API_ENDPOINTS = {
  USERS: '/api/users',
  TRANSFERS: '/api/transfers',
  TRANSACTIONS: '/api/transactions',
  ANALYTICS: '/api/analytics',
  SUMMARY: '/api/summary',
  PEOPLE: '/api/people'
};

// Default fetch options
const DEFAULT_OPTIONS = {
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
};

/**
 * Make an API request
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise} - Promise with response data
 */
async function apiRequest(endpoint, options = {}) {
  try {
    // Merge default options with provided options
    const fetchOptions = {
      ...DEFAULT_OPTIONS,
      ...options
    };
    
    // Make the request
    const response = await fetch(`${API_BASE_URL}${endpoint}`, fetchOptions);
    
    // Handle non-2xx responses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `API Error: ${response.status} ${response.statusText}`);
    }
    
    // Parse and return the response data
    return await response.json();
  } catch (error) {
    console.error(`API request failed for ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Build a query string from parameters
 * @param {Object} params - Query parameters
 * @returns {string} - Query string
 */
function buildQueryString(params = {}) {
  const queryParams = [];
  
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        // Handle array parameters
        value.forEach(item => {
          queryParams.push(`${encodeURIComponent(key)}=${encodeURIComponent(item)}`);
        });
      } else {
        queryParams.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
      }
    }
  });
  
  return queryParams.length > 0 ? `?${queryParams.join('&')}` : '';
}

// API Methods

/**
 * Get users with optional filtering
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with users data
 */
async function getUsers(params = {}) {
  const queryString = buildQueryString(params);
  return apiRequest(`${API_ENDPOINTS.USERS}${queryString}`);
}

/**
 * Get a single user by ID
 * @param {number|string} userId - User ID
 * @returns {Promise} - Promise with user data
 */
async function getUserById(userId) {
  return apiRequest(`${API_ENDPOINTS.USERS}/${userId}`);
}

/**
 * Get transfers with optional filtering
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with transfers data
 */
async function getTransfers(params = {}) {
  const queryString = buildQueryString(params);
  return apiRequest(`${API_ENDPOINTS.TRANSFERS}${queryString}`);
}

/**
 * Get a single transfer by ID
 * @param {number|string} transferId - Transfer ID
 * @returns {Promise} - Promise with transfer data
 */
async function getTransferById(transferId) {
  return apiRequest(`${API_ENDPOINTS.TRANSFERS}/${transferId}`);
}

/**
 * Create a new transfer
 * @param {Object} transferData - Transfer data
 * @returns {Promise} - Promise with created transfer
 */
async function createTransfer(transferData) {
  return apiRequest(API_ENDPOINTS.TRANSFERS, {
    method: 'POST',
    body: JSON.stringify(transferData)
  });
}

/**
 * Get transactions with optional filtering
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with transactions data
 */
async function getTransactions(params = {}) {
  const queryString = buildQueryString(params);
  return apiRequest(`${API_ENDPOINTS.TRANSACTIONS}${queryString}`);
}

/**
 * Get a single transaction by ID
 * @param {number|string} transactionId - Transaction ID
 * @returns {Promise} - Promise with transaction data
 */
async function getTransactionById(transactionId) {
  return apiRequest(`${API_ENDPOINTS.TRANSACTIONS}/${transactionId}`);
}

/**
 * Get analytics data
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with analytics data
 */
async function getAnalytics(params = {}) {
  const queryString = buildQueryString(params);
  return apiRequest(`${API_ENDPOINTS.ANALYTICS}${queryString}`);
}

/**
 * Get summary statistics
 * @returns {Promise} - Promise with summary data
 */
async function getSummary() {
  return apiRequest(API_ENDPOINTS.SUMMARY);
}

/**
 * Get people data (combined from multiple sources)
 * @param {Object} params - Query parameters
 * @returns {Promise} - Promise with people data
 */
async function getPeople(params = {}) {
  const queryString = buildQueryString(params);
  return apiRequest(`${API_ENDPOINTS.PEOPLE}${queryString}`);
}

// Error handling utils

/**
 * Display an API error to the user
 * @param {Error} error - Error object
 * @param {Element} containerElement - Element to display error in
 */
function displayApiError(error, containerElement) {
  if (!containerElement) return;
  
  const errorMessage = error.message || 'An unexpected error occurred';
  
  containerElement.innerHTML = `
    <div class="alert alert-danger" role="alert">
      <i class="fas fa-exclamation-circle me-2"></i>
      ${errorMessage}
    </div>
  `;
}

/**
 * Show a loading spinner
 * @param {Element} containerElement - Element to display spinner in
 */
function showLoadingSpinner(containerElement) {
  if (!containerElement) return;
  
  containerElement.innerHTML = `
    <div class="d-flex justify-content-center align-items-center p-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <span class="ms-2">Loading data...</span>
    </div>
  `;
}

// Export all API utilities
window.api = {
  // Core methods
  request: apiRequest,
  buildQueryString,
  
  // Entity-specific methods
  users: {
    getAll: getUsers,
    getById: getUserById
  },
  transfers: {
    getAll: getTransfers,
    getById: getTransferById,
    create: createTransfer
  },
  transactions: {
    getAll: getTransactions,
    getById: getTransactionById
  },
  analytics: {
    get: getAnalytics
  },
  summary: {
    get: getSummary
  },
  people: {
    getAll: getPeople
  },
  
  // UI helpers
  displayError: displayApiError,
  showLoading: showLoadingSpinner,
  
  // Constants
  endpoints: API_ENDPOINTS
};