import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const TransactionsStatsSection = ({ transactions }) => {
  const navigate = useNavigate();

  const calculateStats = () => {
    const itemCounts = {};
    const storeSales = {};

    transactions.forEach(transaction => {
      transaction.items.forEach(item => {
        itemCounts[item.item] = (itemCounts[item.item] || 0) + item.quantity;
        storeSales[transaction.store] = (storeSales[transaction.store] || 0) + item.quantity;
      });
    });

    return { itemCounts, storeSales };
  };

  const { itemCounts, storeSales } = calculateStats();

  const handleStoreClick = (storeName) => {
    navigate(`/stores/${storeName}/people`, { state: { store: storeName } });
  };

  // New handler for bar chart clicks on an item.
  const handleItemClick = (itemName) => {
    navigate(`/items/${itemName}/stats`, { state: { item: itemName } });
  };

  return (
    <div className="flex flex-col space-y-6">
      <h1 className="text-2xl font-bold text-center">Transaction Statistics</h1>

      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold">Items Sold Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={Object.entries(itemCounts).map(([name, value]) => ({ name, value }))}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar 
              dataKey="value" 
              fill="#8884d8" 
              cursor="pointer"
              onClick={(data) => handleItemClick(data.payload.name)}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold">Sales by Store</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={Object.entries(storeSales).map(([name, value]) => ({ name, value }))}
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#82ca9d"
              label
              style={{ cursor: 'pointer' }}
              onClick={(data) => handleStoreClick(data.name)}
            >
              {Object.entries(storeSales).map((_, index) => (
                <Cell key={index} fill={['#FF8042', '#0088FE', '#FFBB28', '#00C49F'][index % 4]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TransactionsStatsSection;
