import React from 'react';

export const Table = ({ children, className }) => (
  <table className={className}>
    {children}
  </table>
);

export const TableHead = ({ children, className }) => (
  <thead className={className}>
    {children}
  </thead>
);

export const TableBody = ({ children, className }) => (
  <tbody className={className}>
    {children}
  </tbody>
);

export const TableRow = ({ children, className, onClick }) => (
  <tr className={className} onClick={onClick}>
    {children}
  </tr>
);

export const TableCell = ({ children, className }) => (
  <td className={className}>
    {children}
  </td>
);

export const TableHeader = ({ children, className }) => (
  <th className={className}>
    {children}
  </th>
);
