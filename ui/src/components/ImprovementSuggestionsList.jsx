// src/components/ImprovementSuggestionsList.jsx

import React from 'react';

export default function ImprovementSuggestionsList({ loading, suggestionMessages }) {
  return (
    <div className="bg-gray-50 p-4 rounded-md shadow-inner">
      <h2 className="text-lg font-semibold mb-2">Improvement Suggestions</h2>
      <div className="overflow-y-auto border border-gray-300 rounded-md p-2 max-h-40">
        {loading ? (
          <p className="text-center">Loading suggestions...</p>
        ) : suggestionMessages.length === 0 ? (
          <p className="text-center">No suggestions available.</p>
        ) : (
          <ul className="space-y-2">
            {suggestionMessages.map((msg, idx) => (
              <li key={idx} className="p-2 border border-gray-200 rounded-md">
                {msg}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
