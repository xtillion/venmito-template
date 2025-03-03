const ctx = document.getElementById('myChart');

// Fetch data from the server using api
function generateRandomColors(dataLength) {
    const randomColors = [];
    
    for (let i = 0; i < dataLength; i++) {
      const r = Math.floor(Math.random() * 256); 
      const g = Math.floor(Math.random() * 200); 
      const b = Math.floor(Math.random() * 150);
  
      randomColors.push(`rgb(${r}, ${g}, ${b})`); // Push the random color to the array
    }
  
    return randomColors;
  }
  
fetch('/api/citycount')
    .then(response => response.json())  
    .then(data => {
        const backgroundColor = generateRandomColors(data.x.length);
    
        const ctx = document.getElementById('userCities');
        new Chart(ctx, {
            type: 'bar',  
            data: {
                labels: data.x,  
                datasets: [{
                    label: 'Total Users',
                    data: data.y,  
                    borderWidth: 1,
                    backgroundColor: backgroundColor
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Users Per City', 
                        font: {
                            size: 18,  
                            weight: 'bold',  
                            family: 'Arial, sans-serif'
                        },
                        padding: {
                            bottom: 20  
                        }
                    },
                },    
                scales: {
                    y: {
                        beginAtZero: true  
                    }
                },
                maintainAspectRatio: false 
            }
        });
    })
    .catch(error => {
        console.error('Error fetching city count data:', error);
    });

fetch('/api/countrycount')
  .then(response => response.json())
  .then(data => {
        const backgroundColor = generateRandomColors(data.x.length);

      const ctx = document.getElementById('userCountries');

      new Chart(ctx, {
          type: 'doughnut', 
          data: {
              labels: data.x, 
              datasets: [{
                  label: 'Total Users',
                  data: data.y,  
                  borderWidth: 1,
                  backgroundColor: backgroundColor
              }]
          },
          options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Users Per Country',
                    font: {
                        size: 18,  
                        weight: 'bold',
                        family: 'Arial, sans-serif'
                    },
                    padding: {
                        bottom: 20
                    }
                },
            },
              scales: {
                  y: {
                      beginAtZero: true  
                  }
              },
              maintainAspectRatio: false 
          }
      });
  })
  .catch(error => {
      console.error('Error fetching city count data:', error);
  });

  fetch('/api/devicedistrib')
  .then(response => response.json())  
  .then(data => {
      const labels = Object.keys(data); 
      const values = Object.values(data);

      const ctx = document.getElementById('deviceDistribution');
      
      new Chart(ctx, {
          type: 'doughnut', 
          data: {
              labels: labels,
              datasets: [{
                  label: 'Device Count',
                  data: values, 
                  borderWidth: 1
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false,  
              plugins: {
                title: {
                    display: true,
                    text: 'Device Distribution of Users',  
                    font: {
                        size: 18,  
                        weight: 'bold',  
                        family: 'Arial, sans-serif'  
                    },
                    padding: {
                        bottom: 20  
                    }
                },
                tooltip: {
                      callbacks: {
                          label: function(tooltipItem) {
                              return `${tooltipItem.label}: ${tooltipItem.raw}`; 
                          }
                      }
                  }
              }
          }
      });
  })
  .catch(error => {
      console.error('Error fetching device count data:', error);
  });

  fetch('/api/internationTransfer')
  .then(response => response.json())  
  .then(data => {
      const labels = Object.keys(data); 
      const values = Object.values(data); 

      const ctx = document.getElementById('internationTransfer');
      
      new Chart(ctx, {
          type: 'pie',
          data: {
              labels: labels,  
              datasets: [{
                  label: 'Total Transfers',
                  data: values,  
                  borderWidth: 1
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                    display: true,
                    text: 'Domestic vs International Transfers', 
                    font: {
                        size: 18, 
                        weight: 'bold', 
                        family: 'Arial, sans-serif'
                    },
                    padding: {
                        bottom: 20  
                    }
                },
                tooltip: {
                      callbacks: {
                          label: function(tooltipItem) {
                              return `${tooltipItem.label}: ${tooltipItem.raw}`; 
                          }
                      }
                  }
              }
          }
      });
  })
  .catch(error => {
      console.error('Error fetching device count data:', error);
  });
  
  fetch('/api/promoResponse')
  .then(response => response.json())  
  .then(data => {
      const labels = Object.keys(data);  
      const backgroundColor = generateRandomColors(labels.length);
      const values = Object.values(data); 
      const ctx = document.getElementById('promoResponse');
      new Chart(ctx, {
          type: 'bar',  
          data: {
              labels: labels,  
              datasets: [{
                  label: 'Promotion Responses',
                  data: values,  
                  borderWidth: 1,
                  backgroundColor: backgroundColor,
                  barPercentage: 0.5,
                  barThickness: 200         
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false, 
              plugins: {
                title: {
                    display: true,
                    text: 'Promotion Responses',
                    font: {
                        size: 18, 
                        weight: 'bold',  
                        family: 'Arial, sans-serif'
                    },
                    padding: {
                        bottom: 20 
                    }
                },
                tooltip: {
                      callbacks: {
                          label: function(tooltipItem) {
                              return `${tooltipItem.label}: ${tooltipItem.raw}`;  
                          }
                      }
                  }
              }
          }
      });
  })
  .catch(error => {
      console.error('Error fetching device count data:', error);
  });
