import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import DocumentUpload from './DocumentUpload';
import DocumentVerify from './DocumentVerify';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Navigation Bar */}
        <nav className="bg-white shadow-lg mb-8">
          <div className="container mx-auto px-4">
            <div className="flex justify-center space-x-4 py-4">
              <Link
                to="/"
                className="px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors"
              >
                Upload Documents
              </Link>
              <Link
                to="/verify"
                className="px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors"
              >
                Verify Documents
              </Link>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <main className="container mx-auto px-4">
          <Routes>
            <Route path="/" element={<DocumentUpload />} />
            <Route path="/verify" element={<DocumentVerify />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;