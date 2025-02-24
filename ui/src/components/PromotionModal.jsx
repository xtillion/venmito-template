import React from 'react';
import { Dialog, DialogContent, DialogTitle } from '../components/ui/dialog';
import { Table, TableHead, TableHeader, TableBody, TableRow, TableCell } from '../components/ui/table';
import { Button } from '../components/ui/button';

const PromotionModal = ({ selectedPerson, promoInfo, onClose }) => {
  return (
    <Dialog open={!!selectedPerson} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent>
        <DialogTitle>Promotion Info</DialogTitle>
        {promoInfo && promoInfo.length > 0 ? (
          <Table className="w-full border border-gray-300 mt-4">
            <TableHead>
              <TableRow className="bg-gray-200 border border-gray-300">
                <TableHeader className="font-semibold px-4 py-2 border border-gray-300 text-center">
                  Promotion
                </TableHeader>
                <TableHeader className="font-semibold px-4 py-2 border border-gray-300 text-center">
                  Responded
                </TableHeader>
              </TableRow>
            </TableHead>
            <TableBody>
              {promoInfo.map((promo, index) => (
                <TableRow key={index} className="border border-gray-300">
                  <TableCell className="px-4 py-2 text-center border border-gray-300">
                    {promo.promotion}
                  </TableCell>
                  <TableCell className="px-4 py-2 text-center border border-gray-300">
                    {promo.responded}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <p className="mt-4 text-center">This person hasn't been promoted.</p>
        )}
        <Button onClick={onClose} className="mt-4 bg-gray-700 hover:bg-gray-800 text-white">Close</Button>
      </DialogContent>
    </Dialog>
  );
};

export default PromotionModal;
