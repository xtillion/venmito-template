import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableRow } from './ui/table';

export default function DetailedResponsesTable({ loading, detailsData }) {
  const [expandedRows, setExpandedRows] = useState({});

  const toggleRow = (personId) => {
    setExpandedRows(prev => ({
      ...prev,
      [personId]: !prev[personId],
    }));
  };

  return (
    <div className="bg-gray-50 p-4 rounded-md shadow-inner mt-6">
      <h2 className="text-lg font-semibold text-center mb-2">Detailed Responses</h2>
      <div className="overflow-x-auto rounded-md mx-auto max-h-64 w-full">
        {loading ? (
          <p className="text-center p-2">Loading details...</p>
        ) : (
          <Table className="table-fixed w-full border border-gray-300 mx-auto">
            <TableBody>
              <TableRow className="bg-gray-200 border border-gray-300">
                <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                  Name
                </TableCell>
                <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                  Email
                </TableCell>
                <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                  Response
                </TableCell>
              </TableRow>
              {detailsData.map(person => (
                <React.Fragment key={person.person_id}>
                  <TableRow
                    className="hover:bg-gray-200 cursor-pointer"
                    onClick={() => toggleRow(person.person_id)}
                  >
                    <TableCell className="px-4 py-2 border border-gray-300 text-center">
                      {person.first_name} {person.last_name}
                    </TableCell>
                    <TableCell className="px-4 py-2 border border-gray-300 text-center">
                      {person.email}
                    </TableCell>
                    <TableCell className="px-4 py-2 border border-gray-300 text-center">
                      {person.responded}
                    </TableCell>
                  </TableRow>
                  {expandedRows[person.person_id] && (
                    <TableRow>
                        <div className="flex flex-col space-y-4 space-x-4">
                          <div className="flex items-center">
                            <span className="font-semibold w-24">Country:</span>
                            <span>{person.country}</span>
                          </div>
                          <div className="flex items-center">
                            <span className="font-semibold w-24">Devices:</span>
                            <span>
                              {Array.isArray(person.devices)
                                ? person.devices.join(', ')
                                : person.devices}
                            </span>
                          </div>
                        </div>
                    </TableRow>
                  )}
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
