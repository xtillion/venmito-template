import React from 'react';

export const Input = ({ type, placeholder, value, onChange, className }) => (
  <input 
    type={type} 
    placeholder={placeholder} 
    value={value} 
    onChange={onChange} 
    className={`input ${className || ''} border p-2 rounded w-full`}
  />
);
