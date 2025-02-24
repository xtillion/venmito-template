import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import PromotionStatsPage from './pages/PromotionStatsPage';
import StoreCustomerStatsPage from './pages/StoreCustomerStatsPage';
import ItemStatsPage from './pages/ItemStatsPage';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/promotion-chart/:promotionName" element={<PromotionStatsPage />} />
      <Route path="/stores/:storeName/people" element={<StoreCustomerStatsPage />} />
      <Route path="/items/:itemName/stats" element={<ItemStatsPage />} />
    </Routes>
  );
};

export default AppRoutes;
