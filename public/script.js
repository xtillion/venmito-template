const ctx = document.getElementById('myChart');

// Fetch data from the server (API route)
// Fetch the city count data from the server
fetch('/api/citycount')
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        const ctx = document.getElementById('myChart');

        new Chart(ctx, {
            type: 'bar',  // Change the type to your preferred chart type (e.g., 'bar', 'line', etc.)
            data: {
                labels: data.x,  // City names (x axis)
                datasets: [{
                    label: 'City Count',
                    data: data.y,  // City counts (y axis)
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true  // Ensure the y-axis starts at 0
                    }
                },
                maintainAspectRatio: false  // Optional: set to false to allow chart resizing
            }
        });
    })
    .catch(error => {
        console.error('Error fetching city count data:', error);
    });

fetch('/api/countrycount')
  .then(response => response.json())  // Parse the JSON response
  .then(data => {
      const ctx = document.getElementById('myChartTwo');

      new Chart(ctx, {
          type: 'doughnut',  // Change the type to your preferred chart type (e.g., 'bar', 'line', etc.)
          data: {
              labels: data.x,  // City names (x axis)
              datasets: [{
                  label: 'Users Per Country',
                  data: data.y,  // City counts (y axis)
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true  // Ensure the y-axis starts at 0
                  }
              },
              maintainAspectRatio: false  // Optional: set to false to allow chart resizing
          }
      });
  })
  .catch(error => {
      console.error('Error fetching city count data:', error);
  });

