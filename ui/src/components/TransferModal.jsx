import React from 'react';
import { Dialog, DialogContent, DialogTitle } from '../components/ui/dialog';
import { Table, TableBody, TableRow, TableCell } from '../components/ui/table';
import { Button } from '../components/ui/button';

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  };

const TransfersModal = ({ transfer, type, onClose }) => {
  return (
    <Dialog open={!!transfer} onOpenChange={(open) => { if (!open) onClose(); }}>
      <DialogContent>
        <DialogTitle>Transfer Details</DialogTitle>
        {transfer ? (
          <Table className="w-full border border-gray-300 mt-4">
            <TableBody>
              {type === "received" ? (
                <>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Name</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_name}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Email</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_email}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Telephone</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_telephone}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Name</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_name}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Email</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_email}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Telephone</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_telephone}</TableCell>
                  </TableRow>
                </>
              ) : (
                <>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Name</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_name}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Email</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_email}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Sender Telephone</TableCell>
                    <TableCell className="px-4 py-2">{transfer.sender_telephone}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Name</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_name}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Email</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_email}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="px-4 py-2 font-semibold">Recipient Telephone</TableCell>
                    <TableCell className="px-4 py-2">{transfer.recipient_telephone}</TableCell>
                  </TableRow>
                </>
              )}
              <TableRow>
                <TableCell className="px-4 py-2 font-semibold">Amount</TableCell>
                <TableCell className="px-4 py-2">${transfer.amount}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="px-4 py-2 font-semibold">Transfer Date</TableCell>
                <TableCell className="px-4 py-2">{formatDate(transfer.transfer_date)}</TableCell>
                </TableRow>
            </TableBody>
          </Table>
        ) : (
          <p className="mt-4 text-center">No transfer data available.</p>
        )}
        <Button onClick={onClose} className="mt-4 bg-gray-700 hover:bg-gray-800 text-white">
          Close
        </Button>
      </DialogContent>
    </Dialog>
  );
};

export default TransfersModal;
