async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    return response.json();
}



async function updateOverview() {
    const stores = await fetchData('/stores/top');
    const promotions = await fetchData('/clients/promotions');
    const transfers = await fetchData('/clients/top-transfers');
    
    document.getElementById('top-store-revenue').textContent = `$${stores[0]?.Total_Revenue || 0}`;
    document.getElementById('total-promotions').textContent = promotions.length;
    document.getElementById('highest-transfer').textContent = `$${transfers[0]?.Total_Transferred || 0}`;
}


async function updateAvgTransaction() {
    const response = await fetch('/earnings/avg-transaction');
    const data = await response.json();

    if (data.length > 0) {
        document.getElementById('avg-transaction').innerText = `$${data[0].Avg_Transaction_Value.toFixed(2)}`;
    }
}
document.addEventListener('DOMContentLoaded', updateAvgTransaction);

async function createCharts() {
    const stores = await fetchData('/stores/top');
    const storeNames = stores.map(s => s.Store);
    const storeRevenues = stores.map(s => s.Total_Revenue);

    new Chart(document.getElementById('lineChart'), {
        type: 'bar',
        data: {
            labels: storeNames,
            datasets: [{
                label: 'Store Revenue',
                data: storeRevenues,
                backgroundColor: '#ff8600',
                borderColor: '#ff8600',
                borderWidth: 1
            }]
        },
        options: { responsive: true }
    });

    const transfers = await fetchData('/clients/top-transfers');
    const clientNames = transfers.map(t => `${t.First_Name} ${t.Last_Name}`);
    const transferAmounts = transfers.map(t => t.Total_Transferred);

    new Chart(document.getElementById('doughnut'), {
        type: 'polarArea',
        data: {
            labels: clientNames,
            datasets: [{
                label: 'Top Transfers',
                data: transferAmounts,
                backgroundColor: ['yellow', '#5480b9', '#e74c3c', '#8e44ad', '#f39c12'],
            }]
        },
        options: { responsive: true }
    });

    await createStoreSalesChart();
}

async function createStoreSalesChart() {
    const salesData = await fetchData('/stores/sales');

    // Extract all 12 months from the response
    const months = salesData.map(s => s.Month);

    // Get total sales for each month
    const totalSales = salesData.map(s => s.Total_Sales);

    new Chart(document.getElementById('salesChart'), {
        type: 'line',
        data: {
            labels: months, // X-axis: 12 months
            datasets: [{
                label: "Total Monthly Sales",
                data: totalSales, // Y-axis: Total Sales for each month
                borderColor: "#ff8600",
                backgroundColor: "rgb(174, 184, 254, 0.6)",
                fill: true, // Fills area under the line
                tension: 0.3 // Makes it a smooth curve
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                x: { title: { display: true, text: 'Month' } },
                y: { title: { display: true, text: 'Total Sales ($)' } }
            }
        }
    });
}

// Function to generate random colors
function getRandomColor() {
    return `hsl(${Math.floor(Math.random() * 360)}, 70%, 50%)`;
}

updateOverview();
createCharts();

document.getElementById("downloadCsvBtn").addEventListener("click", async function () {
    const response = await fetch("/download-csv");  // Fetch CSV from Flask route
    const data = await response.blob();  // Convert response to Blob

    // Create a download link
    const url = window.URL.createObjectURL(data);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data.csv"; // File name
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});