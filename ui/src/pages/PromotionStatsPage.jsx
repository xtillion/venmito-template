// src/pages/PromotionStatsPage.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { fetchPromotionDetails, fetchImprovementSuggestions } from '../services/api';
import { Button } from '../components/ui/button';

// Child components
import ResponseSummaryChart from '../components/ResponseSummaryChart';
import ImprovementSuggestionsList from '../components/ImprovementSuggestionsList';
import DetailedResponsesTable from '../components/DetailedResponsesTable';

export default function PromotionStatsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const promotion = location.state?.promotion || 'Unknown Promotion';
  const responses = location.state?.responses || []; // Default empty array to prevent errors

  // Calculate summary counts safely
  const yesCount = responses?.filter(r => r.responded?.toLowerCase() === 'yes').length || 0;
  const noCount = responses?.filter(r => r.responded?.toLowerCase() === 'no').length || 0;
  const totalCount = yesCount + noCount;

  // Data for the pie chart summary
  const pieData = [
    { name: 'Yes', value: yesCount },
    { name: 'No', value: noCount },
  ];

  // Detailed Responses
  const [showDetails, setShowDetails] = useState(false);
  const [detailsData, setDetailsData] = useState([]);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const toggleDetails = async () => {
    if (!showDetails && detailsData.length === 0) {
      setLoadingDetails(true);
      try {
        const data = await fetchPromotionDetails(promotion);
        setDetailsData(data || []);
      } catch (error) {
        console.error('Error fetching detailed promotion data:', error);
      } finally {
        setLoadingDetails(false);
      }
    }
    setShowDetails(prev => !prev);
  };

  // Improvement Suggestions
  const [improvementSuggestions, setImprovementSuggestions] = useState([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);

  useEffect(() => {
    const getSuggestions = async () => {
      setLoadingSuggestions(true);
      try {
        const suggestionsData = await fetchImprovementSuggestions(promotion);
        setImprovementSuggestions(suggestionsData || []);
      } catch (error) {
        console.error('Error fetching improvement suggestions:', error);
      } finally {
        setLoadingSuggestions(false);
      }
    };
    getSuggestions();
  }, [promotion]);

  // Flatten suggestions to just suggestion messages
  const suggestionMessages = improvementSuggestions?.flatMap(group =>
    group.metric_values?.map(mv => mv.suggestion) || []
  );

  return (
    <div className="w-full p-6 bg-white rounded-lg shadow-lg overflow-y-auto max-w-4xl mx-auto mt-6">
      <h1 className="text-2xl font-bold text-center mb-6">
        {promotion} Responses
      </h1>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Pie Chart Summary */}
        <ResponseSummaryChart 
          totalCount={totalCount} 
          pieData={pieData} 
        />

        {/* Improvement Suggestions */}
        <ImprovementSuggestionsList 
          loading={loadingSuggestions}
          suggestionMessages={suggestionMessages}
        />
      </div>

      {/* Detailed Responses */}
      {showDetails && (
        <DetailedResponsesTable 
          loading={loadingDetails}
          detailsData={detailsData}
        />
      )}

      {/* Buttons */}
      <div className="flex flex-col sm:flex-row justify-end space-y-6 sm:space-y-0 sm:space-x-4 mt-6">
        <Button 
          onClick={toggleDetails} 
          className="bg-gray-700 hover:bg-gray-800 text-white px-4 py-2 rounded"
        >
          {showDetails ? 'Hide Detailed Responses' : 'Show Detailed Responses'}
        </Button>
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
