import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const ChevronIcon = ({ isExpanded }) => (
    <svg
        className={`h-5 w-5 transition-transform ${isExpanded ? 'transform rotate-180' : ''}`}
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
    >
        <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
        />
    </svg>
);

const DocumentCard = ({ result }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleExpand = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className="result-card">
            <h3>{result.filename}</h3>
            <p className="document-type">Type: {result.document_type}</p>
            <div className="extracted-data">
                {Object.entries(JSON.parse(result.extracted_data)).map(([key, value]) => (
                    <div key={key} className="data-row">
                        <span className="data-label">{key.replace(/_/g, ' ').toUpperCase()}: </span>
                        <span className="data-value">{value}</span>
                    </div>
                ))}
            </div>
            <button onClick={toggleExpand}>
                {isExpanded ? (
                    <ChevronIcon isExpanded={isExpanded} />
                ) : (
                    <ChevronIcon isExpanded={false} />
                )}
            </button>
        </div>
    );
};

const DocumentVerify = () => {
    const [verificationResults, setVerificationResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchAllVerifications();
    }, []);

    const fetchAllVerifications = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.get('http://localhost:8000/api/verify/');
            
            setVerificationResults(response.data);
        } catch (err) {
            const errorMessage = err.response?.status === 404 
                ? 'Verification endpoint not found. Please check API configuration.'
                : err.response?.data?.detail || 'Failed to fetch verification results';
            setError(errorMessage);
            console.error('Error fetching verifications:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="verify-container">
            <h2>Document Verifications</h2>
            
            <button onClick={fetchAllVerifications} disabled={loading}>
                {loading ? 'Loading...' : 'Refresh Results'}
            </button>

            {error && <p className="error">{error}</p>}
            
            {verificationResults.map((result, index) => (

                <DocumentCard key={index} result={result} />
            ))}

            <style>{`
                .verify-container {
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 2rem;
                }

                .result-card {
                    margin: 1rem 0;
                    padding: 1rem;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: #f8f9fa;
                }

                .document-type {
                    color: #666;
                    font-style: italic;
                }

                .extracted-data {
                    margin-top: 1rem;
                    padding: 1rem;
                    background-color: #fff;
                    border-radius: 4px;
                    overflow-x: auto;
                }

                pre {
                    margin: 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }

                button {
                    background-color: #0070f3;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-bottom: 1rem;
                }

                button:disabled {
                    background-color: #ccc;
                }

                .error {
                    color: red;
                    margin: 1rem 0;
                }
            `}</style>
        </div>
    );
};

export default DocumentVerify;