async function fetchCustomerData() {
    const response = await fetch('/customers/data');
    const customers = await response.json();

    // Update cards
    document.getElementById('total-customers').textContent = customers.length;
    document.getElementById('most-active-customer').textContent = customers[0]?.Customer || "-";
    document.getElementById('top-spender').textContent = `$${customers[0]?.Total_Spent.toFixed(2) || 0}`;

    // Populate table
    const tableBody = document.getElementById('customer-data');
    tableBody.innerHTML = "";
    customers.forEach(customer => {
        const row = `<tr>
            <td>${customer.Customer}</td>
            <td>${customer.Transactions}</td>
            <td>$${customer.Total_Spent.toFixed(2)}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

    // Create customer spending chart
    createCustomerSpendingChart(customers);
}

// Customer Spending Chart
function createCustomerSpendingChart(customers) {
    const names = customers.map(c => c.Customer);
    const spending = customers.map(c => c.Total_Spent);

    new Chart(document.getElementById('customerSpendingChart'), {
        type: 'bar',
        data: {
            labels: names,
            datasets: [{
                label: 'Total Spent ($)',
                data: spending,
                backgroundColor: "#ff8600"
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true },
                x: { title: { display: true, text: 'Customers' } }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", fetchCustomerData);