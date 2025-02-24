import React, { useState, useEffect, useMemo } from 'react';
import { Button } from '../components/ui/button';
import { AnimatePresence, motion } from 'framer-motion';
import { fetchTransfers } from '../services/api';
import TransfersModal from '../components/TransferModal';
import TransfersTable from '../components/TransfersTable';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

// Helper function to format date.
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
};

const renderCustomizedLabel = (props) => {
    const { x, y, value, name, cx, cy, midAngle, outerRadius } = props;
    
    // Position label
    const RADIAN = Math.PI / 180;
    const radius = outerRadius + 20; // position the label further out
    const xPos = cx + radius * Math.cos(-midAngle * RADIAN);
    const yPos = cy + radius * Math.sin(-midAngle * RADIAN);
  
    // Truncate location if it's too long
    const truncatedName = name.length > 12 ? name.slice(0, 12) + '…' : name;
  
    return (
      <text
        x={xPos}
        y={yPos}
        fill="black"
        textAnchor={xPos > cx ? 'start' : 'end'}
        dominantBaseline="central"
        style={{ fontSize: '12px' }}
      >
        {truncatedName} ({value})
      </text>
    );
  };

  

// Helper function to sort data by a given field and order.
const sortData = (data, field, order) => {
  return [...data].sort((a, b) => {
    let valA = a[field];
    let valB = b[field];

    // Convert date fields to timestamps.
    if (field === 'transfer_date') {
      valA = new Date(valA).getTime();
      valB = new Date(valB).getTime();
    }

    // Convert amount field to float.
    if (field === 'amount') {
      valA = parseFloat(valA);
      valB = parseFloat(valB);
    }

    // Compare numerically if possible.
    if (typeof valA === 'number' && typeof valB === 'number') {
      return order === 'asc' ? valA - valB : valB - valA;
    }

    // Otherwise compare as strings.
    valA = valA ? valA.toString().toLowerCase() : "";
    valB = valB ? valB.toString().toLowerCase() : "";
    if (valA < valB) return order === 'asc' ? -1 : 1;
    if (valA > valB) return order === 'asc' ? 1 : -1;
    return 0;
  });
};

const TransfersSections = () => {
  // Unified transfers state.
  const [transfers, setTransfers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Received transfers table state.
  const [showReceived, setShowReceived] = useState(true);
  const [receivedSearch, setReceivedSearch] = useState("");
  const [receivedSortField, setReceivedSortField] = useState("recipient_name");
  const [receivedSortOrder, setReceivedSortOrder] = useState("asc");

  // Sent transfers table state.
  const [showSent, setShowSent] = useState(true);
  const [sentSearch, setSentSearch] = useState("");
  const [sentSortField, setSentSortField] = useState("sender_name");
  const [sentSortOrder, setSentSortOrder] = useState("asc");

  // Modal state.
  const [modalData, setModalData] = useState(null); // { transfer, type }

  // Fetch transfers.
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchTransfers();
        setTransfers(data);
      } catch (error) {
        console.error("Error fetching transfers:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Sorting handlers.
  const handleSortReceived = (field) => {
    console.log("Sorting received transfers by", field);
    if (receivedSortField === field) {
      setReceivedSortOrder(receivedSortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setReceivedSortField(field);
      setReceivedSortOrder('asc');
    }
  };

  const handleSortSent = (field) => {
    console.log("Sorting sent transfers by", field);
    if (sentSortField === field) {
      setSentSortOrder(sentSortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSentSortField(field);
      setSentSortOrder('asc');
    }
  };

  // Memoized sorted data for received transfers.
  const sortedReceived = useMemo(() => {
    return sortData(
      transfers.filter((transfer) =>
        transfer.recipient_name.toLowerCase().includes(receivedSearch.toLowerCase())
      ),
      receivedSortField,
      receivedSortOrder
    );
  }, [transfers, receivedSearch, receivedSortField, receivedSortOrder]);

  // Memoized sorted data for sent transfers.
  const sortedSent = useMemo(() => {
    return sortData(
      transfers.filter((transfer) =>
        transfer.sender_name.toLowerCase().includes(sentSearch.toLowerCase())
      ),
      sentSortField,
      sentSortOrder
    );
  }, [transfers, sentSearch, sentSortField, sentSortOrder]);

  // Define columns for the Received Transfers table.
  const receivedColumns = [
    { label: "Recipient Name", field: "recipient_name" },
    { label: "Amount", field: "amount" },
    { label: "Recipient City", field: "recipient_city" },
    { label: "Recipient Country", field: "recipient_country" },
    { label: "Transfer Date", field: "transfer_date" },
  ];

  // Define columns for the Sent Transfers table.
  const sentColumns = [
    { label: "Sender Name", field: "sender_name" },
    { label: "Amount", field: "amount" },
    { label: "Sender City", field: "sender_city" },
    { label: "Sender Country", field: "sender_country" },
    { label: "Transfer Date", field: "transfer_date" },
  ];

  // Process yearly data for the line graph.
  const yearlyData = useMemo(() => {
    const data = {};
    transfers.forEach((transfer) => {
      const year = new Date(transfer.transfer_date).getFullYear();
      const amt = parseFloat(transfer.amount) || 0;
      if (!data[year]) data[year] = { year, totalAmount: 0 };
      data[year].totalAmount += amt;
    });
    return Object.values(data).sort((a, b) => a.year - b.year);
  }, [transfers]);

  // Process sender data for the pie chart.
  const senderData = useMemo(() => {
    const counts = transfers.reduce((acc, transfer) => {
      const key = `${transfer.sender_city || "Unknown"}, ${transfer.sender_country || "Unknown"}`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    return Object.entries(counts).map(([location, count]) => ({ location, count }));
  }, [transfers]);

  // Process receiver data for the pie chart.
  const receiverData = useMemo(() => {
    const counts = transfers.reduce((acc, transfer) => {
      const key = `${transfer.recipient_city || "Unknown"}, ${transfer.recipient_country || "Unknown"}`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    return Object.entries(counts).map(([location, count]) => ({ location, count }));
  }, [transfers]);

  // Colors for the pie charts.
  const pieColors = ['#FF8042', '#0088FE', '#FFBB28', '#00C49F', '#AF19FF', '#FF4560'];

  return (
    <div className="flex flex-col space-y-6 p-8 bg-white rounded-lg shadow-lg max-w-5xl mx-auto mt-6">
      <h1 className="text-3xl font-bold text-center">Transfers</h1>

      {/* Received Transfers Table Container */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Received Transfers</h2>
          <Button
            className="bg-gray-700 hover:bg-gray-800 text-white"
            onClick={() => setShowReceived(!showReceived)}
          >
            {showReceived ? "Hide" : "Show"} Received Transfers
          </Button>
        </div>
        <AnimatePresence>
          {showReceived && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              {loading ? (
                <p className="text-center py-4">Loading transfers...</p>
              ) : (
                <TransfersTable
                  title="Received Transfers"
                  columns={receivedColumns}
                  data={sortedReceived}
                  searchPlaceholder="Search by recipient name..."
                  searchValue={receivedSearch}
                  onSearchChange={(e) => setReceivedSearch(e.target.value)}
                  onSort={handleSortReceived}
                  sortField={receivedSortField}
                  sortOrder={receivedSortOrder}
                  onRowClick={(transfer) =>
                    setModalData({ transfer, type: "received" })
                  }
                  formatDate={formatDate}
                />
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Sent Transfers Table Container */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Sent Transfers</h2>
          <Button
            className="bg-gray-700 hover:bg-gray-800 text-white"
            onClick={() => setShowSent(!showSent)}
          >
            {showSent ? "Hide" : "Show"} Sent Transfers
          </Button>
        </div>
        <AnimatePresence>
          {showSent && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              {loading ? (
                <p className="text-center py-4">Loading transfers...</p>
              ) : (
                <TransfersTable
                  title="Sent Transfers"
                  columns={sentColumns}
                  data={sortedSent}
                  searchPlaceholder="Search by sender name..."
                  searchValue={sentSearch}
                  onSearchChange={(e) => setSentSearch(e.target.value)}
                  onSort={handleSortSent}
                  sortField={sentSortField}
                  sortOrder={sentSortOrder}
                  onRowClick={(transfer) =>
                    setModalData({ transfer, type: "sent" })
                  }
                  formatDate={formatDate}
                />
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Yearly Transfers Line Graph Container */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-center mb-4">Yearly Transfer Amount</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={yearlyData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="totalAmount" stroke="#0088FE" name="Total Amount" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Sender Pie Chart Container */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-center mb-4">Sender Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={senderData}
              dataKey="count"
              nameKey="location"
              cx="50%"
              cy="50%"
              outerRadius={120}
              label={renderCustomizedLabel}
            >
              {senderData.map((entry, index) => (
                <Cell key={`cell-sender-${index}`} fill={pieColors[index % pieColors.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Receiver Pie Chart Container */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-center mb-4">Receiver Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={receiverData}
              dataKey="count"
              nameKey="location"
              cx="50%"
              cy="50%"
              outerRadius={120}
              label={renderCustomizedLabel}
            >
              {receiverData.map((entry, index) => (
                <Cell key={`cell-receiver-${index}`} fill={pieColors[index % pieColors.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {modalData && (
        <TransfersModal
          transfer={modalData.transfer}
          type={modalData.type}
          onClose={() => setModalData(null)}
        />
      )}
    </div>
  );
};

export default TransfersSections;
