import React from 'react';

export const Dialog = ({ open, onOpenChange, children }) => {
  if (!open) return null;
  return (
    <div className="dialog-overlay fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="dialog-content bg-white rounded shadow-lg">
        {children}
      </div>
    </div>
  );
};

export const DialogContent = ({ children }) => (
  <div className="p-4">
    {children}
  </div>
);

export const DialogTitle = ({ children }) => (
  <h2 className="text-xl font-bold mb-4">
    {children}
  </h2>
);
