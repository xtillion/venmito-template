// src/components/ResponseSummaryChart.jsx

import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const COLORS = ['#00C49F', '#FF8042'];

export default function ResponseSummaryChart({ totalCount, pieData }) {
  return (
    <div className="bg-gray-50 p-4 rounded-md shadow-inner flex flex-col items-center">
      <h2 className="text-lg font-semibold mb-2">Response Summary</h2>
      {totalCount === 0 ? (
        <p className="text-center">No data available.</p>
      ) : (
        <div style={{ width: 330, height: 330 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent, value }) =>
                  `${name}: ${value} (${(percent * 100).toFixed(0)}%)`
                }
                labelLine={false}
                paddingAngle={2}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend layout="horizontal" align="center" verticalAlign="bottom" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
