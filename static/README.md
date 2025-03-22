# Venmito Dark Theme Implementation

This package provides a dark theme and improved layout for the Venmito application. The theme features a sophisticated dark color palette with colorful accents for better data visualization and user experience.

## Files Included

1. **dark-theme.css** - Main stylesheet for the dark theme
2. **layout.html** - Base template with updated navbar (navigation now on the right)
3. **analytics.html** - Updated analytics page with stats cards and proper chart sizing
4. **analytics.js** - JavaScript for chart initialization with dark theme colors
5. **common.js** - Shared utility functions across all pages
6. **app.py** - Flask application with routes and mock data
7. **dashboard.html** - Homepage with overview stats and recent activity

## Implementation Instructions

### 1. Directory Structure

Place the files in the following directory structure:

```
venmito-template/
├── static/
│   ├── css/
│   │   └── dark-theme.css
│   └── js/
│       ├── analytics.js
│       └── common.js
├── templates/
│   ├── layout.html
│   ├── dashboard.html
│   └── analytics.html
└── app.py
```

### 2. Setting Up the Dark Theme

1. Add the dark-theme.css file to your static/css directory
2. Replace your existing layout.html with the provided version
3. Update your page templates to use the new layout and styling

### 3. Chart Sizing Guide

The theme includes several predefined chart container classes for consistent sizing:

- `.chart-container-sm` - 200px height (use for small charts)
- `.chart-container-md` - 300px height (use for medium charts)
- `.chart-container-lg` - 400px height (use for large charts)
- `.chart-container-xl` - 500px height (use for full-width visualizations)

Example usage:
```html
<div class="chart-container-md">
    <canvas id="my-chart"></canvas>
</div>
```

### 4. Stats Cards

The theme includes styled stats cards with accent colors:

```html
<div class="stats-card blue-accent">
    <div class="stats-title">Title</div>
    <div class="stats-value">Value</div>
    <div class="stats-change positive">
        <i class="fas fa-arrow-up"></i> x% change
    </div>
</div>
```

Available accent classes:
- `blue-accent`
- `green-accent`
- `yellow-accent`
- `red-accent`
- `purple-accent`
- `teal-accent`

### 5. Connecting the API

The application includes mock data and API endpoints for development. To connect to real data:

1. Update the API routes in `app.py` to connect to your actual data sources
2. Uncomment the API fetch functions in `analytics.js` to use real data
3. Replace the mock data in tables with dynamic data from your backend

Example for updating the API connection:

```javascript
// In analytics.js or your custom JavaScript file
fetchFromAPI(API_ENDPOINTS.SUMMARY).then(data => {
  // Update DOM elements with the real data
  document.querySelector('.total-users .stats-value').textContent = formatNumber(data.total_users);
  document.querySelector('.total-transfers .stats-value').textContent = formatCurrency(data.total_transfers);
  // etc.
});
```

### 6. Customizing the Theme

You can customize the theme colors by modifying the CSS variables at the top of `dark-theme.css`:

```css
:root {
  /* Main theme colors */
  --bg-primary: #121212;     /* Main background */
  --bg-secondary: #1e1e1e;   /* Card backgrounds */
  --bg-tertiary: #2d2d2d;    /* Headers, table rows */
  --text-primary: #ffffff;   /* Main text */
  --text-secondary: #b3b3b3; /* Secondary text */
  --text-muted: #8c8c8c;     /* Muted text */
  
  /* Accent colors - modify these to match your brand */
  --accent-blue: #4285f4;
  --accent-green: #34a853;
  --accent-yellow: #fbbc05;
  --accent-red: #ea4335;
  --accent-purple: #ab47bc;
  --accent-teal: #26a69a;
}
```

## Additional Tips

### Chart.js Configuration

The dark theme includes preset colors for Chart.js. When creating new charts, use these colors for consistency:

```javascript
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

// Use in your chart configuration
datasets: [{
  label: 'My Data',
  data: [42, 45, 38, 40, 48, 52],
  borderColor: chartColors.blue,
  backgroundColor: 'rgba(66, 133, 244, 0.2)'
}]
```

### Responsive Design

The theme is fully responsive and will adapt to different screen sizes. For the best experience:

- Use the provided grid classes from Bootstrap
- Use the responsive chart containers
- Test on multiple device sizes

## Troubleshooting

### Charts Not Displaying Correctly

If charts aren't displaying with the correct styling:

1. Make sure you've included Chart.js before your custom JS
2. Check that the chart container has a defined height
3. Verify that the canvas element has the correct ID

### API Connection Issues

If you're having trouble connecting to the API:

1. Check browser console for errors
2. Verify API endpoint URLs
3. Ensure your API returns data in the expected format
4. Check for CORS issues if API is on a different domain

## License

This theme and implementation guide is provided for use with the Venmito project.