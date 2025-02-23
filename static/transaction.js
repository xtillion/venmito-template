async function fetchTransactions() {
    const response = await fetch('/transactions/data');
    const transactions = await response.json();

    // Update summary cards
    document.getElementById('total-transactions').textContent = transactions.length;
    document.getElementById('total-transaction-value').textContent = `$${transactions.reduce((sum, t) => sum + t.Amount_USD, 0).toFixed(2)}`;
    
    if (transactions.length > 0) {
        document.getElementById('avg-transaction').textContent = `$${(transactions.reduce((sum, t) => sum + t.Amount_USD, 0) / transactions.length).toFixed(2)}`;
        document.getElementById('top-transaction').textContent = `$${Math.max(...transactions.map(t => t.Amount_USD)).toFixed(2)}`;
    }

    // Populate transaction table
    const tableBody = document.getElementById('transaction-data');
    tableBody.innerHTML = "";
    transactions.forEach(t => {
        const row = `<tr>
            <td>${t.First_Name} ${t.Last_Name}</td>
            <td>${t.Store}</td>
            <td>$${t.Amount_USD.toFixed(2)}</td>
            <td>${t.Transfer_Date}</td>
            <td>${t.Payment_Method || 'Unknown'}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });

    // Create transaction trends chart
    createTransactionChart(transactions);
}

// Chart for transactions over time
async function createTransactionChart(transactions) {
    const months = [...new Set(transactions.map(t => t.Transfer_Date.slice(0, 7)))];
    const salesData = months.map(month => 
        transactions.filter(t => t.Transfer_Date.startsWith(month))
                    .reduce((sum, t) => sum + t.Amount_USD, 0)
    );

    new Chart(document.getElementById('transactionChart'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Total Monthly Transactions ($)',
                data: salesData,
                borderColor: "#ff8600",
                backgroundColor: "rgb(174, 184, 254, 0.6)",
                fill: true,
                tension: 0.3
            }]
        }
    });
}

document.addEventListener("DOMContentLoaded", fetchTransactions);