import React from 'react';
import { Card, CardContent } from './ui/card';
import { Table, TableBody, TableRow, TableCell } from './ui/table';
import { Input } from './ui/input';

const TransfersTable = ({
  title,
  columns,
  data,
  searchPlaceholder,
  searchValue,
  onSearchChange,
  onSort,
  sortField,
  sortOrder,
  onRowClick,
  formatDate,
}) => {
  // Helper to render sort indicator.
  const renderSortIndicator = (currentField, field, order) => {
    if (currentField !== field) return null;
    return order === 'asc' ? ' ↑' : ' ↓';
  };

  return (
    <Card>
      <CardContent>
        <h2 className="text-lg font-semibold mb-2 text-center">{title}</h2>
        <Input
          type="text"
          placeholder={searchPlaceholder}
          value={searchValue}
          onChange={onSearchChange}
          className="mb-4"
        />
        <Table className="w-full border border-gray-300">
          <TableBody>
            <TableRow className="bg-gray-200 border border-gray-300">
              {columns.map((col, index) => (
                <TableCell
                  key={index}
                  className="font-semibold px-4 py-2 border border-gray-300 text-center"
                >
                  <span
                    onClick={() => onSort(col.field)}
                    className="cursor-pointer select-none"
                  >
                    {col.label}
                    {renderSortIndicator(sortField, col.field, sortOrder)}
                  </span>
                </TableCell>
              ))}
            </TableRow>
            {data.map((row, index) => (
              <TableRow
                key={index}
                className="border cursor-pointer hover:bg-gray-200"
                onClick={() => onRowClick(row)}
              >
                {columns.map((col, idx) => (
                  <TableCell
                    key={idx}
                    className="px-4 py-2 border border-gray-300 text-center"
                  >
                    {col.field === 'transfer_date'
                      ? formatDate(row[col.field])
                      : row[col.field]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default TransfersTable;
