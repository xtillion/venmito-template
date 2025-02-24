import React from 'react';

export const Card = ({ children, className }) => (
  <div className={`card ${className || ''} border rounded shadow bg-white`}>
    {children}
  </div>
);

export const CardContent = ({ children, className }) => (
  <div className={`card-content ${className || ''} p-4`}>
    {children}
  </div>
);
