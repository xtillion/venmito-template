import React from 'react';

export const Button = ({ children, onClick, className = '', noDefaultPadding = false }) => (
  <button 
    type="button" 
    onClick={onClick} 
    className={`${className} ${noDefaultPadding ? '' : 'p-2'} rounded cursor-pointer`}
  >
    {children}
  </button>
);


