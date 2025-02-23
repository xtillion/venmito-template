async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    return response.json();
}

async function loadCharts() {
    const revenueData = await fetchData('/analytics/revenue-trend');
    const transactionData = await fetchData('/analytics/transaction-distribution');

    const months = revenueData.map(d => d.Month);
    const revenues = revenueData.map(d => d.Total_Revenue);

    new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: "Total Revenue",
                data: revenues,
                borderColor: "#ff8600",
                backgroundColor: "rgb(174, 184, 254, 0.6)",
                fill: true
            }]
        }
    });

    const storeNames = transactionData.map(t => t.Store);
    const transactions = transactionData.map(t => t.Num_Transactions);

    new Chart(document.getElementById('transactionChart'), {
        type: 'bar',
        data: {
            labels: storeNames,
            datasets: [{
                label: "Number of Transactions",
                data: transactions,
                backgroundColor: "#ff8600"
            }]
        }
    });
}

async function loadPromotionAnalysis() {
    const promotions = await fetchData('/clients/promotions-analysis');
    const analysisContainer = document.getElementById('promotion-analysis');

    // Clear existing rows
    analysisContainer.innerHTML = "";

    promotions.forEach(p => {
        const row = `<tr>
                        <td>${p.promotion}</td>
                        <td>${p.Count}</td>
                        <td>${p.Percentage}%</td>
                    </tr>`;
        analysisContainer.innerHTML += row;
    });
}

// Run the function when the page loads
document.addEventListener('DOMContentLoaded', loadPromotionAnalysis);

async function loadCustomers() {
    const customers = await fetchData('/customers/top');
    const tableBody = document.getElementById('customer-data');

    // Clear existing rows
    tableBody.innerHTML = "";

    customers.forEach(c => {
        const row = `<tr>
                        <td>${c.Customer}</td>
                        <td>${c.Transactions}</td>
                        <td>$${c.Total_Spent.toFixed(2)}</td>
                        <td>${c.Promotion}</td> <!-- Show promotion -->
                    </tr>`;
        tableBody.innerHTML += row;
    });

    makeTableSortable();
}

document.addEventListener('DOMContentLoaded', () => {
    loadCharts();
    loadCustomers();
});