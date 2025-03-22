/**
 * Venmito Common JavaScript
 * Shared functionality across all pages
 */

// Initialize tooltips and popovers if Bootstrap is present
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
      });
    }
  
    // Initialize Bootstrap popovers
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
      const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
      popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
      });
    }
  });
  
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
   * Format date to a readable string
   * @param {string} dateString - ISO date string
   * @param {boolean} includeTime - Whether to include time
   * @returns {string} - Formatted date string
   */
  function formatDate(dateString, includeTime = false) {
    if (!dateString) return '-';
    
    const date = new Date(dateString);
    
    const options = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      ...(includeTime && {
        hour: '2-digit',
        minute: '2-digit'
      })
    };
    
    return date.toLocaleDateString('en-US', options);
  }
  
  /**
   * Show loading spinner in an element
   * @param {Element} element - The element to show spinner in
   * @param {string} size - Size of spinner (sm, md, lg)
   */
  function showLoadingSpinner(element, size = 'md') {
    if (!element) return;
    
    const sizeClass = size === 'sm' ? 'spinner-border-sm' : 
                      size === 'lg' ? 'spinner-border-lg' : '';
    
    const spinner = `
      <div class="text-center p-3">
        <div class="spinner-border ${sizeClass} text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-secondary">Loading data...</p>
      </div>
    `;
    
    element.innerHTML = spinner;
  }
  
  /**
   * Show error message in an element
   * @param {Element} element - The element to show error in
   * @param {string} message - Error message
   */
  function showErrorMessage(element, message = 'Failed to load data. Please try again.') {
    if (!element) return;
    
    const errorHtml = `
      <div class="alert alert-danger" role="alert">
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
      </div>
    `;
    
    element.innerHTML = errorHtml;
  }
  
  /**
   * Debounce a function call to prevent too frequent executions
   * @param {Function} func - The function to debounce
   * @param {number} delay - Delay in milliseconds
   * @returns {Function} - Debounced function
   */
  function debounce(func, delay = 300) {
    let timeoutId;
    
    return function(...args) {
      const context = this;
      
      clearTimeout(timeoutId);
      
      timeoutId = setTimeout(() => {
        func.apply(context, args);
      }, delay);
    };
  }
  
  // Export utilities for use in other modules if needed
  window.venmito = {
    formatCurrency,
    formatNumber,
    formatDate,
    showLoadingSpinner,
    showErrorMessage,
    debounce
  };