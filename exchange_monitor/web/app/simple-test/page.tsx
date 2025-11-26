'use client';

export default function SimpleTestPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Simple Test Page</h1>
      
      {/* Test 1: Basic div */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 1: Basic Div</h2>
        <div className="h-[400px] w-full border-2 border-red-500 bg-gray-100 flex items-center justify-center">
          <p className="text-lg">This is a basic div test</p>
        </div>
      </div>

      {/* Test 2: SVG */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 2: SVG</h2>
        <div className="h-[400px] w-full border-2 border-blue-500 bg-gray-50">
          <svg width="100%" height="100%" viewBox="0 0 600 400">
            <rect x="50" y="50" width="100" height="100" fill="red" />
            <circle cx="300" cy="200" r="50" fill="blue" />
            <text x="300" y="350" textAnchor="middle" fontSize="20">SVG Test</text>
          </svg>
        </div>
      </div>

      {/* Test 3: Canvas */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Test 3: Canvas</h2>
        <div className="h-[400px] w-full border-2 border-green-500 bg-gray-50">
          <canvas width="600" height="400" style={{ border: '1px solid black' }}>
            Your browser does not support the canvas element.
          </canvas>
        </div>
      </div>
    </div>
  );
} 