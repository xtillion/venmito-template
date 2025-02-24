import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { 
  fetchPromotedPeople, 
  fetchTransactions, 
  fetchTransfers, 
  fetchPromoInfo 
} from '../services/api';
import CustomersWithPromotionsSection from '../sections/CustomersWithPromotionSection';
import TransactionsStatsSection from '../sections/TransactionsStatsSection';
import TransfersSections from '../sections/TransfersSections';

export default function Dashboard() {
  const [people, setPeople] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [selectedPerson, setSelectedPerson] = useState(null);
  const [promoInfo, setPromoInfo] = useState([]);
  const [view, setView] = useState('promotions');

  useEffect(() => {
    const loadData = async () => {
      try {
        const peopleData = await fetchPromotedPeople();
        setPeople(peopleData);
        const transactionsData = await fetchTransactions();
        setTransactions(transactionsData);
      } catch (error) {
        console.error(error);
      }
    };
    loadData();
  }, []);

  const handlePersonClick = async (personId) => {
    try {
      const promoData = await fetchPromoInfo(personId);
      setPromoInfo(promoData);
      setSelectedPerson(personId);
    } catch (error) {
      console.error(error);
    }
  };

  // JSON download logic
  const handleDownloadJSON = async () => {
    try {
      let data = [];
      let filename = 'data.json';

      if (view === 'promotions') {
        data = people;
        filename = 'promotions.json';
      } else if (view === 'transactions') {
        data = transactions;
        filename = 'transactions.json';
      } else if (view === 'transfers') {
        data = await fetchTransfers();
        filename = 'transfers.json';
      } else {
        alert('No JSON available for this view.');
        return;
      }

      if (!Array.isArray(data) || data.length === 0) {
        alert('No data available to export.');
        return;
      }

      const jsonString = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading JSON:', error);
      alert('Failed to download JSON.');
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6 bg-gray-100 rounded-lg shadow-lg">
      <Navbar view={view} setView={setView} onDownload={handleDownloadJSON} />
      <h1 className="text-2xl font-bold text-center">Venmito Dashboard</h1>
      {view === 'promotions' && (
        <CustomersWithPromotionsSection 
          people={people} 
          onPersonClick={handlePersonClick} 
          selectedPerson={selectedPerson} 
          promoInfo={promoInfo} 
          setSelectedPerson={setSelectedPerson} 
        />
      )}
      {view === 'transactions' && <TransactionsStatsSection transactions={transactions} />}
      {view === 'transfers' && <TransfersSections />}
    </div>
  );
}
