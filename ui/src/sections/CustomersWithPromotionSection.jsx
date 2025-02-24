import React, { useState } from 'react';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { AnimatePresence, motion } from 'framer-motion';
import CustomersWithPromotionTable from '../components/CustomersWithPromotionTable';
import PromotionModal from '../components/PromotionModal';
import PromotionsPieChart from '../components/PromotionsPieChart';

const CustomersWithPromotionsSection = ({ people, onPersonClick, selectedPerson, promoInfo, setSelectedPerson }) => {
  const [showPeople, setShowPeople] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div>
      <Button
        className="mt-4 bg-gray-700 hover:bg-gray-800 text-white"
        onClick={() => setShowPeople(!showPeople)}
      >
        {showPeople ? 'Hide' : 'Show'} Customers With Promotions
      </Button>

      <AnimatePresence>
        {showPeople && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden space-y-6 mt-4"
          >
            <Input
              type="text"
              placeholder="Search people by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="mt-4"
            />
            <CustomersWithPromotionTable
              people={people}
              searchQuery={searchQuery}
              onPersonClick={onPersonClick}
            />
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex justify-center mt-6">
        <PromotionsPieChart />
      </div>

      <PromotionModal
        selectedPerson={selectedPerson}
        promoInfo={promoInfo}
        onClose={() => setSelectedPerson(null)}
      />
    </div>
  );
};

export default CustomersWithPromotionsSection;
