'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const data = [
  { name: 'A', value: 10 },
  { name: 'B', value: 20 },
  { name: 'C', value: 15 },
  { name: 'D', value: 25 }
];

export default function TestChartPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Recharts Test</h1>
      
      {/* Test 1: Fixed size chart */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 1: Fixed Size Chart</h2>
        <div style={{ width: '600px', height: '400px', border: '2px solid red' }}>
          <BarChart width={600} height={400} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </div>
      </div>

      {/* Test 2: ResponsiveContainer */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 2: ResponsiveContainer</h2>
        <div className="h-[400px] w-full border-2 border-blue-500">
          <BarChart width={600} height={400} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#82ca9d" />
          </BarChart>
        </div>
      </div>

      {/* Test 3: Simple div */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 3: Simple Div</h2>
        <div className="h-[400px] w-full border-2 border-green-500 bg-gray-100 flex items-center justify-center">
          <p className="text-lg">This is a test div with border</p>
        </div>
      </div>
    </div>
  );
} 