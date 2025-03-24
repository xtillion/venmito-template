import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router";
import { useState } from "react";
import HomePage from "./pages/HomePage";
import ClientInsightsPage from "./pages/ClientInsightsPage";
import ItemInsightsPage from "./pages/ItemsInsightsPage";

import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/client-insights" element={<ClientInsightsPage />} />
        <Route path="/item-insights" element={<ItemInsightsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
