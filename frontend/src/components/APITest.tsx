import React, { useState } from 'react';
import { runAPITest } from '../tests/api.test';

const APITest: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runTest = async () => {
    setIsRunning(true);
    setResult(null);
    setError(null);

    try {
      const success = await runAPITest();
      setResult(success ? 'All tests passed successfully!' : 'Tests failed');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">API Connection Test</h2>
      <button
        onClick={runTest}
        disabled={isRunning}
        className={`px-4 py-2 rounded ${
          isRunning
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        {isRunning ? 'Running Tests...' : 'Run API Test'}
      </button>

      {result && (
        <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
          {result}
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default APITest; 