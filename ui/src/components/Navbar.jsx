import React from 'react';
import { Button } from '../components/ui/button';

const Navbar = ({ view, setView, onDownload }) => {
  return (
    <nav className="flex items-center justify-between p-4 bg-gray-700 text-white rounded-lg shadow-md">
      {/* Left container: Save JSON Button */}
      <div className="flex items-center">
        <Button
          onClick={onDownload}
          className="px-5 py-2 rounded-md font-semibold transition-all bg-gray-600 hover:bg-gray-500 text-white min-w-[120px] cursor-pointer flex items-center space-x-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2}
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 11-6 0v-1m6-4V5a3 3 0 00-6 0v5" 
            />
          </svg>
          <span>Save JSON</span>
        </Button>
      </div>

      {/* Center container: Navigation Buttons */}
      <div className="flex space-x-4">
        <Button 
          onClick={() => setView('promotions')} 
          className={`px-6 py-2 rounded-md font-semibold transition-all ${
            view === 'promotions'
              ? 'bg-blue-500 text-white shadow-lg scale-105'
              : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
          }`}
        >
          Promotions
        </Button>
        <Button 
          onClick={() => setView('transactions')} 
          className={`px-6 py-2 rounded-md font-semibold transition-all ${
            view === 'transactions'
              ? 'bg-blue-500 text-white shadow-lg scale-105'
              : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
          }`}
        >
          Transactions
        </Button>
        <Button 
          onClick={() => setView('transfers')} 
          className={`px-6 py-2 rounded-md font-semibold transition-all ${
            view === 'transfers'
              ? 'bg-blue-500 text-white shadow-lg scale-105'
              : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
          }`}
        >
          Transfers
        </Button>
      </div>

      {/* Right container: Empty for balance */}
      <div className="w-32"></div>
    </nav>
  );
};

export default Navbar;
