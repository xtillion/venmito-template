/**
 * Main JavaScript file for Venmito dashboard.
 * Contains common utility functions used across the application.
 */

// API constants
const API_BASE_URL = '/api';

// Util functions
const Utils = {
    /**
     * Format a number as currency
     * @param {number} amount - The amount to format
     * @param {string} currency - Currency code (default: USD)
     * @returns {string} Formatted currency string
     */
    formatCurrency: function(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },

    /**
     * Format a date string
     * @param {string} dateString - The date string to format
     * @returns {string} Formatted date string
     */
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    },

    /**
     * Make an API request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise} Promise with JSON response
     */
    fetchAPI: async function(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'API request failed');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    },

    /**
     * Create pagination for tables
     * @param {Element} container - Pagination container element
     * @param {number} currentPage - Current page number
     * @param {number} totalPages - Total number of pages
     * @param {Function} onPageChange - Callback when page is changed
     */
    createPagination: function(container, currentPage, totalPages, onPageChange) {
        // Clear existing pagination
        container.innerHTML = '';
        
        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage <= 1 ? 'disabled' : ''}`;
        const prevLink = document.createElement('a');
        prevLink.className = 'page-link';
        prevLink.href = '#';
        prevLink.textContent = 'Previous';
        if (currentPage > 1) {
            prevLink.addEventListener('click', (e) => {
                e.preventDefault();
                onPageChange(currentPage - 1);
            });
        }
        prevLi.appendChild(prevLink);
        container.appendChild(prevLi);
        
        // Page numbers
        const maxPages = 5; // Show at most 5 page numbers
        const startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
        const endPage = Math.min(totalPages, startPage + maxPages - 1);
        
        for (let i = startPage; i <= endPage; i++) {
            const pageLi = document.createElement('li');
            pageLi.className = `page-item ${i === currentPage ? 'active' : ''}`;
            const pageLink = document.createElement('a');
            pageLink.className = 'page-link';
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.addEventListener('click', (e) => {
                e.preventDefault();
                if (i !== currentPage) {
                    onPageChange(i);
                }
            });
            pageLi.appendChild(pageLink);
            container.appendChild(pageLi);
        }
        
        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage >= totalPages ? 'disabled' : ''}`;
        const nextLink = document.createElement('a');
        nextLink.className = 'page-link';
        nextLink.href = '#';
        nextLink.textContent = 'Next';
        if (currentPage < totalPages) {
            nextLink.addEventListener('click', (e) => {
                e.preventDefault();
                onPageChange(currentPage + 1);
            });
        }
        nextLi.appendChild(nextLink);
        container.appendChild(nextLi);
    },

    /**
     * Show loading indicator in a container
     * @param {Element} container - Container element
     * @param {string} message - Loading message
     */
    showLoading: function(container, message = 'Loading...') {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="loading-spinner mb-3"></div>
                <p>${message}</p>
            </div>
        `;
    },

    /**
     * Show error message in a container
     * @param {Element} container - Container element
     * @param {string} message - Error message
     */
    showError: function(container, message) {
        container.innerHTML = `
            <div class="alert alert-danger my-3" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                ${message}
            </div>
        `;
    },

    /**
     * Get common chart options
     * @param {boolean} responsive - Whether chart should be responsive
     * @returns {Object} Chart.js options object
     */
    getChartOptions: function(responsive = true) {
        return {
            responsive: responsive,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            }
        };
    },

    /**
     * Generate a random color
     * @returns {string} Random RGB color string
     */
    getRandomColor: function() {
        const r = Math.floor(Math.random() * 200);
        const g = Math.floor(Math.random() * 200);
        const b = Math.floor(Math.random() * 200);
        return `rgb(${r}, ${g}, ${b})`;
    },

    /**
     * Generate an array of chart colors
     * @param {number} count - Number of colors to generate
     * @returns {Array} Array of color strings
     */
    generateChartColors: function(count) {
        // Pre-defined color palette for consistency
        const palette = [
            'rgb(54, 162, 235)', // blue
            'rgb(255, 99, 132)', // red
            'rgb(75, 192, 192)', // green
            'rgb(255, 159, 64)', // orange
            'rgb(153, 102, 255)', // purple
            'rgb(255, 205, 86)', // yellow
            'rgb(201, 203, 207)' // grey
        ];
        
        const colors = [];
        
        // Use palette colors first, then generate random colors if needed
        for (let i = 0; i < count; i++) {
            if (i < palette.length) {
                colors.push(palette[i]);
            } else {
                colors.push(this.getRandomColor());
            }
        }
        
        return colors;
    }
};

// Set active nav item based on current page
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    const navItems = document.querySelectorAll('.navbar-nav .nav-link');
    
    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href === path) {
            item.classList.add('active');
        }
    });
});