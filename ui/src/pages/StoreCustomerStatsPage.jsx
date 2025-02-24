import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import { fetchStoreCustomers } from '../services/api';
import { Button } from '../components/ui/button';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, Legend } from 'recharts';
import { AnimatePresence, motion } from 'framer-motion';

export default function StoreCustomerStatsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { name } = useParams(); // Fallback to route param
  const storeName = location.state?.store || name || 'Unknown Store';

  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedCustomer, setExpandedCustomer] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      setLoading(true);
      try {
        const response = await fetchStoreCustomers(storeName);
        if (response && Array.isArray(response.customers)) {
          setCustomers(response.customers);
        } else {
          setCustomers([]); // Ensure customers is always an array
        }
      } catch (error) {
        console.error('Error fetching customers:', error);
        setCustomers([]); // Handle API errors gracefully
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, [storeName]);

  const toggleCustomerDetails = (customerId) => {
    setExpandedCustomer(expandedCustomer === customerId ? null : customerId);
  };

  // Compute customer statistics
  const cityDistribution = {};
  const customerSpending = {};
  const customerItemCount = {};

  customers.forEach(customer => {
    const city = customer.city;
    cityDistribution[city] = (cityDistribution[city] || 0) + 1;

    const fullName = `${customer.first_name} ${customer.last_name}`;
    let totalSpent = 0;
    let totalItems = 0;

    if (Array.isArray(customer.transactions)) {
      totalSpent = customer.transactions.reduce((acc, transaction) => {
        // Sum the total_price of all items within the transaction
        const transactionTotal = transaction.items.reduce((sum, item) => sum + item.total_price, 0);
        return acc + transactionTotal;
      }, 0);
      
      totalItems = customer.transactions.reduce((acc, transaction) => {
        // Sum the quantity of all items within the transaction
        const itemsCount = transaction.items.reduce((sum, item) => sum + item.quantity, 0);
        return acc + itemsCount;
      }, 0);
    }
    customerSpending[fullName] = totalSpent;
    customerItemCount[fullName] = totalItems;
  });

  const cityData = Object.entries(cityDistribution).map(([name, value]) => ({ name, value }));
  const spendingData = Object.entries(customerSpending).map(([name, value]) => ({ name, value }));
  const itemsData = Object.entries(customerItemCount).map(([name, value]) => ({ name, value }));

  // Get top 10 customers for spending and items purchased by sorting descending and slicing
  const topSpendingData = spendingData.sort((a, b) => b.value - a.value).slice(0, 10);
  const topItemsData = itemsData.sort((a, b) => b.value - a.value).slice(0, 10);

  const COLORS = ['#FF8042', '#0088FE', '#FFBB28', '#00C49F', '#AF19FF', '#FF4560'];

  return (
    <div className="w-full p-6 bg-white rounded-lg shadow-lg overflow-y-auto max-w-5xl mx-auto mt-6">
      <h1 className="text-3xl font-bold text-center mb-6">{storeName} - Customer Statistics</h1>

      {/* Pie Chart: Customers per City */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-lg font-semibold text-center mb-4">Customer Distribution by City</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={cityData}
              cx="50%"
              cy="50%"
              outerRadius={100}
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            >
              {cityData.map((_, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart: Top 10 Customers by Spending */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-lg font-semibold text-center mb-4">Top 10 Customers by Spending</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topSpendingData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#0088FE" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart: Top 10 Customers by Items Purchased */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md mb-6">
        <h2 className="text-lg font-semibold text-center mb-4">Top 10 Customers by Items Purchased</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topItemsData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#FF8042" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Customer List */}
      <div className="bg-gray-50 p-4 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold text-center mb-4">Customer Details</h2>
        <AnimatePresence>
          {customers.map((customer) => (
            <motion.div
              key={customer.person_id}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="border-b py-3"
            >
              <div
                className="flex justify-between items-center cursor-pointer p-2 bg-white rounded-md shadow-md hover:bg-gray-100 transition"
                onClick={() => toggleCustomerDetails(customer.person_id)}
              >
                <span className="font-semibold">{customer.first_name} {customer.last_name}</span>
                <span className="text-gray-600">{customer.city}, {customer.country}</span>
              </div>

              {expandedCustomer === customer.person_id && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="p-4 bg-white rounded-md shadow-md mt-2"
                >
                  <p><strong>Email:</strong> {customer.email}</p>
                  <p><strong>Phone:</strong> {customer.telephone}</p>
                  <p>
                    <strong>Total Spent:</strong> $
                    {Array.isArray(customer.transactions)
                      ? customer.transactions.reduce((acc, transaction) =>
                          acc + transaction.items.reduce((sum, item) => sum + item.total_price, 0)
                        , 0)
                      : 0}
                  </p>
                  <p>
                    <strong>Total Items Purchased:</strong> 
                    {Array.isArray(customer.transactions)
                      ? customer.transactions.reduce((acc, transaction) =>
                          acc + transaction.items.reduce((sum, item) => sum + item.quantity, 0)
                        , 0)
                      : 0}
                  </p>
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
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
