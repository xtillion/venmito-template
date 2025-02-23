async function fetchEarningsData() {
    const response = await fetch('/earnings/data');
    const earnings = await response.json();

    // Update summary cards
    const totalRevenue = earnings.reduce((sum, e) => sum + e.Total_Revenue, 0);
    document.getElementById('total-revenue').textContent = `$${totalRevenue.toFixed(2)}`;

    if (earnings.length > 0) {
        document.getElementById('avg-store-revenue').textContent = `$${(totalRevenue / earnings.length).toFixed(2)}`;
        document.getElementById('top-earning-store').textContent = `$${Math.max(...earnings.map(e => e.Total_Revenue)).toFixed(2)}`;
    }

    // Populate earnings table
    const tableBody = document.getElementById('earnings-data');
    tableBody.innerHTML = "";
    earnings.forEach(e => {
        const row = `<tr>
            <td>${e.Store}</td>
            <td>$${e.Total_Revenue.toFixed(2)}</td>
            <td>${e.Num_Transactions}</td>
            <td>$${(e.Total_Revenue / e.Num_Transactions).toFixed(2)}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

// Revenue Trends Chart
async function fetchEarningsTrends() {
    const response = await fetch('/earnings/trends');
    const earnings = await response.json();

    const months = earnings.map(e => e.Month);
    const salesData = earnings.map(e => e.Total_Revenue);

    new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: "Total Monthly Revenue",
                data: salesData,
                borderColor: "#ff8600",
                backgroundColor: "rgb(174, 184, 254, 0.6)",
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    suggestedMax: Math.max(...salesData) + 10,
                    ticks: {
                        stepSize: 10
                    },
                    title: {
                        display: true,
                        text: 'Revenue ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Month'
                    }
                }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    fetchEarningsData();  // ✅ Loads store-level revenue into the table
    fetchEarningsTrends(); // ✅ Loads monthly revenue into the chart
});