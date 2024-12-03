import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import DocumentUpload from './DocumentUpload';
import DocumentVerify from './DocumentVerify';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200">
        {/* Navigation Bar */}
        <nav className="bg-gray-100 shadow-lg mb-8 py-8">
          <div className="container mx-auto px-4">
            <div className="flex justify-end space-y-4 py-4">
              <Link
                to="/"
                className="mx-4 px-8 py-4 rounded-xl bg-white text-gray-700 font-medium
                          shadow-[5px_5px_10px_rgba(0,0,0,0.1),-5px_-5px_10px_rgba(255,255,255,0.8)]
                          hover:shadow-[inset_5px_5px_10px_rgba(0,0,0,0.1),inset_-5px_-5px_10px_rgba(255,255,255,0.8)]
                          transition-all duration-200 transform hover:scale-95"
              >
                <button>Upload Documents</button>
              </Link>
              <Link
                to="/verify"
                className="mx-4 px-8 py-4 rounded-xl bg-white text-gray-700 font-medium
                          shadow-[5px_5px_10px_rgba(0,0,0,0.1),-5px_-5px_10px_rgba(255,255,255,0.8)]
                          hover:shadow-[inset_5px_5px_10px_rgba(0,0,0,0.1),inset_-5px_-5px_10px_rgba(255,255,255,0.8)]
                          transition-all duration-200 transform hover:scale-95"
              >
                <button>Verify Documents</button>
              </Link>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <main className="container mx-auto px-4 flex flex-col items-center justify-center min-h-[calc(100vh-200px)]">
        
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