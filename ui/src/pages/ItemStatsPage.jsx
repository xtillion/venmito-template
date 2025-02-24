import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { Button } from '../components/ui/button';
import { fetchItemTransactions, fetchItemPeopleTransactions } from '../services/api.js';

export default function ItemStatsPage() {
  const { itemName } = useParams();
  const navigate = useNavigate();

  const [transactions, setTransactions] = useState([]);
  const [demographics, setDemographics] = useState(null);
  const [loadingTx, setLoadingTx] = useState(true);
  const [loadingDemo, setLoadingDemo] = useState(true);

  useEffect(() => {
    // Fetch transactions for the item.
    const fetchTransactionsData = async () => {
      try {
        const data = await fetchItemTransactions(itemName);
        setTransactions(data);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      } finally {
        setLoadingTx(false);
      }
    };

    // Fetch demographics for the item buyers.
    const fetchDemographicsData = async () => {
      try {
        const data = await fetchItemPeopleTransactions(itemName);
        setDemographics(data);
      } catch (error) {
        console.error("Error fetching demographics:", error);
      } finally {
        setLoadingDemo(false);
      }
    };

    fetchTransactionsData();
    fetchDemographicsData();
  }, [itemName]);

  // ----------------------------
  // Process the item transactions
  // ----------------------------
  const safeTransactions = Array.isArray(transactions) ? transactions : [];

  // Summation of quantity sold by store
  const storeAggregation = {};
  safeTransactions.forEach((tx) => {
    // Sum the quantity for each item in this transaction.
    const totalQuantity = tx.items.reduce((sum, item) => sum + item.quantity, 0);
    storeAggregation[tx.store] = (storeAggregation[tx.store] || 0) + totalQuantity;
  });

  // Convert to array and sort descending by quantity
  const storeData = Object.entries(storeAggregation).map(([store, quantity]) => ({ store, quantity }));
  storeData.sort((a, b) => b.quantity - a.quantity);

  // Take top 5
  const topStores = storeData.slice(0, 5);

  // ----------------------------
  // Process the demographics
  // ----------------------------
  const safeCustomers = Array.isArray(demographics?.customers) ? demographics.customers : [];

  // Summation of city distribution
  const cityAggregation = {};
  safeCustomers.forEach((customer) => {
    const city = customer.city || "Unknown";
    cityAggregation[city] = (cityAggregation[city] || 0) + 1;
  });
  const cityData = Object.entries(cityAggregation).map(([city, count]) => ({ city, count }));

  // Compute top customers by quantity for this item
  // We also compute how much they spent in total on this item
  const customerMap = {};
  safeCustomers.forEach((customer) => {
    // Construct a unique key for the customer (or just use first+last)
    const fullName = `${customer.first_name} ${customer.last_name}`;
    let totalQuantity = 0;
    let totalSpent = 0;

    if (Array.isArray(customer.transactions)) {
      customer.transactions.forEach((tx) => {
        if (Array.isArray(tx.items)) {
          tx.items.forEach((item) => {
            // Only count the item that matches itemName
            if (item.item_name === itemName) {
              totalQuantity += item.quantity;
              totalSpent += item.total_price;
            }
          });
        }
      });
    }

    if (totalQuantity > 0) {
      customerMap[fullName] = {
        name: fullName,
        quantity: (customerMap[fullName]?.quantity || 0) + totalQuantity,
        spent: (customerMap[fullName]?.spent || 0) + totalSpent,
      };
    }
  });

  // Convert customer map to array and sort by quantity descending
  const customerArray = Object.values(customerMap);
  customerArray.sort((a, b) => b.quantity - a.quantity);

  // Take top 5 customers
  const topCustomers = customerArray.slice(0, 5);

  // Colors for charts
  const colors = ['#FF8042', '#0088FE', '#FFBB28', '#00C49F', '#AF19FF', '#FF4560'];

  return (
    <div className="w-full p-6 bg-white rounded-lg shadow-lg overflow-y-auto max-w-5xl mx-auto mt-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        {itemName} - Sales & Buyer Demographics
      </h1>

      {/* Top Stores Section */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-semibold text-center mb-4">
          Top 5 Stores Selling {itemName}
        </h2>
        {loadingTx ? (
          <p className="text-center">Loading transactions...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topStores}>
              <XAxis dataKey="store" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="quantity" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* NEW: Top Customers Bar Chart */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-semibold text-center mb-4">
          Top 5 Customers for {itemName}
        </h2>
        {loadingDemo ? (
          <p className="text-center">Loading customer data...</p>
        ) : topCustomers.length === 0 ? (
          <p className="text-center">No customers have purchased this item.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topCustomers}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip
          formatter={(value, name) => {
            if (name === 'Total Spent') {
              return [`$${value}`, name];
            }
            return [value, name];
          }}
        />
              <Legend />
              {/* One bar for quantity, one for total spent */}
              <Bar dataKey="quantity" fill="#8884d8" name="Quantity" />
              <Bar dataKey="spent" fill="#82ca9d" name="Total Spent" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Buyer Demographics Section */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-xl font-semibold text-center mb-4">
          Buyer Demographics by City
        </h2>
        {loadingDemo ? (
          <p className="text-center">Loading demographics...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={cityData}
                dataKey="count"
                nameKey="city"
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#82ca9d"
                label
              >
                {cityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Back Button */}
      <div className="flex justify-end mt-6">
        <Button
          onClick={() => navigate(-1)}
          className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded"
        >
          Back
        </Button>
      </div>
    </div>
  );
}
