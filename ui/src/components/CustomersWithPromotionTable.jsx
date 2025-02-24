import React from 'react';
import { Card, CardContent } from './ui/card';
import { Table, TableBody, TableCell, TableRow } from './ui/table';

const CustomersWithPromotionTable = ({ people, searchQuery, onPersonClick }) => {
  const filteredPeople = people.filter(person =>
    `${person.first_name} ${person.last_name}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  // Deduplicate by person_id
  const uniquePeople = Array.from(
    new Map(filteredPeople.map(person => [person.person_id, person])).values()
  );

  return (
    <Card>
      <CardContent>
        <h2 className="text-lg font-semibold mb-2">Customers With Promotion</h2>
        <Table className="w-full border border-gray-300">
          <TableBody>
            <TableRow className="bg-gray-200 border border-gray-300">
              <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                Name
              </TableCell>
              <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                Email
              </TableCell>
              <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                Location
              </TableCell>
              <TableCell className="font-semibold px-4 py-2 border border-gray-300 text-center">
                Phone
              </TableCell>
            </TableRow>

            {uniquePeople.map(person => (
              <TableRow
                key={person.person_id}
                className="border cursor-pointer hover:bg-gray-200"
                onClick={() => onPersonClick(person.person_id)}
              >
                <TableCell className="px-4 py-2 border border-gray-300 text-center">
                  {person.first_name} {person.last_name}
                </TableCell>
                <TableCell className="px-4 py-2 border border-gray-300 text-center">
                  {person.email}
                </TableCell>
                <TableCell className="px-4 py-2 border border-gray-300 text-center">
                  {person.city}, {person.country}
                </TableCell>
                <TableCell className="px-4 py-2 border border-gray-300 text-center">
                  {person.telephone}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
};

export default CustomersWithPromotionTable;
